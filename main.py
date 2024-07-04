import requests
from datetime import datetime
import os

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

GITHUB_API_KEY = os.environ['GITHUB_API_KEY'] 

# Headers para autenticação
headers = {
    'Authorization': f'token {GITHUB_API_KEY}'
}

def get_github_followers(username):
    url = f"https://api.github.com/users/{username}/followers"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        return user_info
    else:
        return None
    
def get_user_details(user):
    url = f'https://api.github.com/users/{user}'
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    username = 'elonmuskceo'
    user_info = get_github_followers(username)
    info = []  

    if user_info:
        followers_list = [follower['login'] for follower in user_info]
        for follower in followers_list:
            a = get_user_details(follower)
            info.append({
                'name': a['name'],
                'blog': a['blog'],
                'company': a['company'].replace('@', '') if a['company'] is not None else None,
                'email': a['email'],
                'bio': a['bio'],
                'public_repos': a['public_repos'],
                'followers': a['followers'],
                'following': a['following'],
                'created_at': datetime.strptime(a['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y"),
            })
    else:
        print("User not found.")

    spark = SparkSession.builder \
            .appName("GitHubUserInfo") \
            .getOrCreate()

    # Define schema for the DataFrame
    schema = StructType([
        StructField('name', StringType(), True),
        StructField('blog', StringType(), True),
        StructField('company', StringType(), True),
        StructField('email', StringType(), True),
        StructField('bio', StringType(), True),
        StructField('public_repos', IntegerType(), True),
        StructField('followers', IntegerType(), True),
        StructField('following', IntegerType(), True),
        StructField('created_at', StringType(), True)
    ])

    df = spark.createDataFrame(info, schema=schema)

    df.show()

    df.write.csv(f'github_followers_{username}.csv', header=True)

    spark.stop()


if __name__ == "__main__":
    main()
# Use uma imagem base oficial do Spark com Hadoop
FROM bitnami/spark:3.3.0

# Corrigir o problema de diretório faltando e instalar dependências do sistema
USER root
RUN mkdir -p /var/lib/apt/lists/partial && \
    apt-get update && \
    apt-get install -y python3-pip && \
    chown -R 1001 /var/lib/apt/lists

# Instalar as bibliotecas Python necessárias
RUN pip3 install requests

# Copiar o script para o container
COPY main.py /opt/spark-apps/

COPY .env .env
RUN export $(cat .env | xargs)

# Definir o diretório de trabalho
WORKDIR /opt/spark-apps/

# Comando para executar o script
CMD ["spark-submit", "main.py"]

FROM python:3.11-slim
WORKDIR /app

# Copy only essential files for minimal run
COPY start_with_integrity.sh ./
COPY rick_institutional_full.py ./
COPY rick_institutional_full.py ./
COPY util ./util
COPY oanda ./oanda
COPY brokers ./brokers
COPY bridges ./bridges
COPY foundation ./foundation
COPY rick_hive ./rick_hive
COPY config ./config
COPY .env.example ./.env

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir requests

EXPOSE 8080

CMD ["bash","start_with_integrity.sh"]

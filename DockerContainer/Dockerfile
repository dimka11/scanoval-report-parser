# app/Dockerfile

FROM python:3.9-slim

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["streamlit", "run", "./StreamlitClient.py", "--server.port=8501", "--server.address=127.0.0.1"]
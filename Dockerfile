FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential libpq-dev ffmpeg && \
    rm -rf /var/lib/apt/lists/*
    
COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

CMD ["flask", "run"]
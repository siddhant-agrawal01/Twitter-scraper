FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y wget gnupg ca-certificates && \
    apt-get install -y chromium && \
    pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "360", "app:app"]
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y chromium chromium-driver --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt

# Create a non-root user
RUN useradd -m myuser
RUN chown -R myuser:myuser /app
USER myuser

# Add these environment variables for Chromium
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMIUM_PATH=/usr/bin/chromium

COPY . .

# Add these Chrome flags to your Python code or set them as environment variables
ENV CHROME_OPTIONS="--headless --no-sandbox --disable-dev-shm-usage --disable-gpu --disable-software-rasterizer"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "360", "app:app"]
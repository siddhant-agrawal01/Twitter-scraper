FROM python:3.9-slim-buster

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget gnupg ca-certificates \
                       fonts-liberation \
                       libappindicator3-1 \
                       libasound2 \
                       libatk-bridge2.0-0 \
                       libatk1.0-0 \
                       libc6 \
                       libcairo2 \
                       libcups2 \
                       libdbus-1-3 \
                       libexpat1 \
                       libfontconfig1 \
                       libgbm1 \
                       libgcc1 \
                       libgconf-2-4 \
                       libgdk-pixbuf2.0-0 \
                       libgl1 \
                       libglib2.0-0 \
                       libgssapi-krb5-2 \
                       libgtk-3-0 \
                       libjpeg62-turbo \
                       libk5crypto3 \
                       libkrb5-3 \
                       libnspr4 \
                       libnss3 \
                       libpango-1.0-0 \
                       libpangocairo-1.0-0 \
                       libpng16-16 \
                       libpulse0 \
                       libstdc++6 \
                       libx11-6 \
                       libx11-xcb1 \
                       libxcb-dri3-0 \
                       libxcb1 \
                       libxcomposite1 \
                       libxcursor1 \
                       libxdamage1 \
                       libxext6 \
                       libxfixes3 \
                       libxi6 \
                       libxrandr2 \
                       libxrender1 \
                       libxss1 \
                       libxtst6 \
                       xdg-utils \
                       xvfb

# Install Chromium (latest stable)
RUN apt-get install -y chromium-browser

# Install correct ChromeDriver version
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip -d /usr/bin/
RUN chmod +x /usr/bin/chromedriver

# Set Chromium binary path
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Start Xvfb
RUN Xvfb :1 -screen 0 1920x1080x24 &
ENV DISPLAY=:1

# Increase Gunicorn timeout
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "360", "app:app"]
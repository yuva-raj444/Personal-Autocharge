#!/bin/bash

echo "🚀 Starting Chrome installation for Render..."

# Update system packages
apt-get update -y

# Install essential packages
apt-get install -y wget curl gnupg unzip software-properties-common

# Install Chrome dependencies first
apt-get install -y \
    libasound2 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libnss3

# Add Google Chrome repository
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list

# Update and install Chrome
apt-get update -y
apt-get install -y google-chrome-stable

# Verify Chrome installation
google-chrome --version || echo "❌ Chrome installation failed"

# Install ChromeDriver with version matching
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+')
echo "📦 Chrome version: $CHROME_VERSION"

# Get compatible ChromeDriver version
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION%%.*}")
echo "📦 ChromeDriver version: $CHROMEDRIVER_VERSION"

# Download and install ChromeDriver
wget -N "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip -o chromedriver_linux64.zip
chmod +x chromedriver
mv chromedriver /usr/local/bin/chromedriver
rm chromedriver_linux64.zip

# Verify ChromeDriver installation
chromedriver --version || echo "❌ ChromeDriver installation failed"

# Create Chrome user directory
mkdir -p /tmp/chrome-user-data
chmod 777 /tmp/chrome-user-data

echo "✅ Chrome and ChromeDriver installation completed"

# Install Python dependencies
pip install -r requirements_render.txt

echo "✅ Build script completed successfully"
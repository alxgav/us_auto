FROM python:3.10.6-slim-buster

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN python -m playwright install chromium

# Install dependencies for Playwright
RUN apt-get update && apt-get -y install \
    curl \
    libnss3 \
    libx11-xcb-dev \
    libxcb-dri3-dev \
    libxcomposite1 \
    libxcursor-dev \
    libxdamage-dev \
    libxi6 \
    libxtst6 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxss1 \
    libgbm-dev \
    libgtk-3-0 \
    libasound2 \
    xvfb

# # Install Playwright
# RUN curl -fsSL https://playwright.dev/python/install.sh | bash

COPY . .
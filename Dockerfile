# syntax=docker/dockerfile:1

FROM python:3
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \
    chromium \
    libnss3 \
    libgconf-2-4 \
    libxi6 \
    libxcursor1 \
    libxss1 \
    libxcomposite1 \
    libasound2 \
    libxrandr2 \
    libgl1-mesa-glx \
    libatk1.0-0 \
    libgtk-3-0 \
    libgbm1 \
    libpango-1.0-0 \
    libdbus-glib-1-2 \
    && rm -rf /var/lib/apt/lists/*
CMD [ "python3", "pynetgear_online_status_manager.py"]

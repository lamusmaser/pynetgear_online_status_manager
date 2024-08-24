# syntax=docker/dockerfile:1

FROM python:3
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python3", "pynetgear_online_status_manager.py"]
FROM python:3.7

COPY . /cloud-app-launcher
RUN python -m pip install -r cloud-app-launcher/requirements.txt
ENV AWS_ACCESS_KEY=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV LAUNCHER_SERVER_PORT="8080"
ENTRYPOINT python /cloud-app-launcher/cloud_launcher/main.py



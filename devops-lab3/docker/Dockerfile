# Lab 3 - container image for the flask app (metrics + logging)
FROM python:3.12-slim

ARG APP_VERSION=3.0.0
ENV APP_VERSION=${APP_VERSION}
ENV LOG_DIR=/var/log/lab3

WORKDIR /app

COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app/ /app/

EXPOSE 5000

RUN mkdir -p /var/log/lab3 && useradd -m appuser && chown -R appuser /var/log/lab3
USER appuser

CMD ["python", "app.py"]

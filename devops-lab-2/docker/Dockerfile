# Lab 2 - container image for the flask app
FROM python:3.12-slim

ARG APP_VERSION=2.0.0
ENV APP_VERSION=${APP_VERSION}

WORKDIR /app

# install dependencies first so this layer is cached
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy application code
COPY app/ /app/

EXPOSE 5000

# run as non-root user
RUN useradd -m appuser
USER appuser

CMD ["python", "app.py"]

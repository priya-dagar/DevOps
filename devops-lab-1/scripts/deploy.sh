#!/bin/bash
# Deploys the flask app to /opt/devops-lab1 and restarts the systemd service
set -e

APP_SRC="$(cd "$(dirname "$0")/.." && pwd)"
APP_DEST="/opt/devops-lab1"

echo "Deploying from $APP_SRC to $APP_DEST ..."

sudo mkdir -p "$APP_DEST"
sudo rm -rf "$APP_DEST/app" "$APP_DEST/tests"
sudo cp -r "$APP_SRC/app" "$APP_SRC/tests" "$APP_DEST/"

cd "$APP_DEST"
if [ ! -d venv ]; then
    python3 -m venv venv
fi
./venv/bin/pip install -q -r app/requirements.txt

sudo systemctl restart devops-lab1.service
sleep 3

STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health || true)
if [ "$STATUS" = "200" ]; then
    echo "Deploy successful - health check returned HTTP $STATUS"
else
    echo "Health check failed (HTTP $STATUS)"
    exit 1
fi

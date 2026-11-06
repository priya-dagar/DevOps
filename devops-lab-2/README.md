# devops-lab-2

ENSP461 - DevOps and Automation, Lab 2: Containerization & Kubernetes Orchestration.

The same Flask application from Lab 1 is containerized with Docker, deployed on a
Minikube Kubernetes cluster, and deployed continuously through the Jenkins CI/CD
pipeline from Lab 1.

## Structure
- app/           - Flask application source code (v2.0.0)
- tests/         - pytest unit tests
- docker/        - Dockerfile, .dockerignore, docker-compose.yml (app + redis)
- k8s/           - ConfigMap, Deployment, Service manifests
- scripts/       - build/push/deploy helper scripts
- docs/          - command logs, screenshots and observations
- reports/       - final lab report PDFs

## Quick commands
docker build -f docker/Dockerfile -t <hubuser>/devops-lab2-app:2.0.0 .
docker compose -f docker/docker-compose.yml up -d
minikube start --driver=docker --memory=2048 --cpus=2 --force-systemd=true
eval $(minikube docker-env) && docker build -f docker/Dockerfile -t devops-lab2-app:2.0.0 .
kubectl apply -f k8s/
minikube service lab2-app-service

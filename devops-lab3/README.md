# devops-lab-3

ENSP461 - DevOps and Automation, Lab 3: Monitoring, Logging & DevSecOps.

The Flask application is now managed with Ansible and Terraform, monitored with
Prometheus/Grafana, its logs centralized with the ELK stack, and secured through
scanning gates in the Jenkins CI/CD pipeline. Feature flags, load testing and
Selenium browser tests complete the workflow.

## Structure
- app/           - Flask application v3.0.0 (/metrics, /beta feature flag, file logging)
- tests/         - pytest unit tests + selenium browser test
- ansible/       - inventory (localhost + docker node) and playbook
- terraform/     - docker provider IaC (init/plan/apply, scalable replicas)
- monitoring/    - prometheus.yml, grafana provisioning, docker-compose (app+prometheus+grafana)
- logging/       - elasticsearch + logstash + kibana compose, logstash pipeline
- security/      - devsecops Jenkinsfile (pip-audit, bandit, trivy)
- docs/          - command logs, screenshots and observations
- reports/       - final lab report PDFs

## Quick commands
# configuration management (q1)
ansible-playbook -i ansible/inventory.ini ansible/playbook.yml

# infrastructure as code (q2)
cd terraform && terraform init && terraform apply -var="replicas=4"

# monitoring stack (q3)
docker compose -f monitoring/docker-compose.yml up -d --build
# app on :5003, prometheus on :9090, grafana on :3300 (dashboard auto-provisioned)

# logging stack (q4)
sudo sysctl -w vm.max_map_count=262144
docker compose -f logging/docker-compose.yml up -d
# elasticsearch :9200, kibana :5601

# devsecops scans (q5) - also run automatically by the Jenkins job devops-lab3-devsecops
./venv/bin/pip-audit -r app/requirements.txt
./venv/bin/python -m bandit -r app/ -q --skip B104
trivy image --severity HIGH,CRITICAL abhinaaav/devops-lab2-app:2.1.3

# feature flag + selenium (q6)
docker run -d -p 5004:5000 -e FEATURE_BETA=true devops-lab3-app:3.0.0
./venv/bin/python tests/selenium_test.py http://localhost:5004

## Pipeline
The Jenkins job devops-lab3-devsecops polls this repository and runs
pip-audit -> bandit -> trivy on every change. Vulnerable dependencies or code
findings block the build (see builds 1-3 in the build history - fixed in later
commits).

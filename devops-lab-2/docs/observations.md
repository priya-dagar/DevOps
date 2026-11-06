# Lab 2 Observations

## Q1 - Containerize with Docker
- The image builds in layers: dependency install (`pip install`) was placed before the code copy so rebuilds reuse the cached dependency layer.
- `docker history` shows each layer with its size; the base image (python:3.12-slim) is most of the 204 MB, the app layers add only a few MB.
- The container runs as a non-root user (`appuser`), which maps to uid 1000 (visible with `docker top`).
- Note: WSL2 + Docker 29.x uses the systemd cgroup driver by default, which breaks the minikube docker driver (runc fails to create the systemd scope). Setting `"exec-opts": ["native.cgroupdriver=cgroupfs"]` in `/etc/docker/daemon.json` fixed it.

## Q2 - Manage containers and images
- `docker stop` keeps the container (shows as Exited in `ps -a`); `start` resumes it. `rm` removes it entirely.
- Tagging with `docker tag` just adds a new name to the same image ID - `abhinaaav/devops-lab2-app:2.0.0` and `devops-lab2-app:2.0.0` shared the digest 66c210e3f934.
- Docker Hub accepted the push with a personal access token via `--password-stdin`; the image appeared on the hub page immediately.
- Docker Compose: `up -d` created its own network (`docker_lab2net`), both services resolved each other by name (`redis` -> 172.19.0.2), and `down` removed everything cleanly.
- Gotcha: the compose `web` service failed to start while the standalone container from Q1 still held port 5000 - port conflicts matter across compose projects too.

## Q3 - Docker storage
- Container-layer data (`/tmp/note.txt`) disappeared after `docker rm` + recreate: writable layers die with the container.
- A named volume (`lab2data`) survived deletion and recreation because it lives in `/var/lib/docker/volumes/`.
- A bind mount (`~/lab2-bindmount-data:/data`) synced both ways: host edits visible in the container, container writes visible on the host.

## Q4 - Docker network
- On a user-defined bridge network, containers resolve each other by **name** through Docker's embedded DNS (`ping net-b` worked) and by **IP** (172.18.0.3).
- On the default `bridge` network there is no embedded DNS - `ping net-a` failed with "Name or service not known".
- The minimal `ubuntu:24.04` image ships without `ping`; `apt install iputils-ping` was needed inside the demo containers.

## Q5 - Deploy to Kubernetes (Minikube)
- Minikube v1.39 on WSL2 needed two fixes: `--force-systemd=true` (minikube issue #20469 - without it the node container exits with code 255) and, empirically, an open WSL session (a `sleep infinity` session keeps the node container alive).
- With the containerd runtime, `eval $(minikube docker-env)` builds are experimental and failed (buildkit 404); `minikube image load` is the supported way to move an image into the cluster.
- Deployment (2 replicas with readiness/liveness probes on `/health`) + NodePort Service (30080) + ConfigMap worked as written; `kubectl rollout status` is a clean way to wait.
- NodePort access works from inside WSL via the node IP (192.168.49.2:30080); from Windows, `kubectl port-forward` to localhost is the easy path.

## Q6 - Rolling update, rollback, scaling
- `kubectl set image` triggered a rolling update: new pods came up one-by-one while old ones terminated - the service stayed available the whole time (captured pod transitions).
- `kubectl rollout undo` returned to the previous image; the version reverted from 2.0.1 to 2.0.0 because the version is baked into the image (build ARG) rather than the ConfigMap.
- Observation: the health curl taken *immediately* after `rollout undo` still returned 2.0.1 for a few seconds - the terminating pods were still registered in the service endpoints.
- `kubectl scale --replicas=4` produced 2 extra Running pods within seconds; scaling back to 2 terminated them cleanly.

## Q7 - Continuous deployment
- The Jenkins user needed docker group membership and a copy of the kubeconfig (with cert paths rewritten into /var/lib/jenkins) - `minikube ip` is not available to the jenkins user, so the pipeline reads the node IP through kubectl instead.
- First CD run failed only at the final health check (the minikube profile issue above); build/push/deploy had already succeeded - fixed in commit `fix CD health check...`.
- A push to `main` is picked up by Poll SCM (H/5) and automatically: builds image `abhinaaav/devops-lab2-app:2.1.<build#>` -> pushes to Docker Hub -> `kubectl set image` -> `rollout status` -> health check. The cluster serves the new version without any manual step.

# Lab 1 Observations

## Q4 - Install and configure Git and Jenkins
- Git 2.43.0 was available in the Ubuntu 24.04 apt repository; `apt install` finished in a few seconds.
- Global config (user.name, user.email, init.defaultBranch) is stored in `~/.gitconfig` and applies to every repo.
- Jenkins 2.580.2 LTS needs **Java 21 or 25** - Java 17 is rejected at startup with a clear message, so openjdk-21-jdk had to be installed.
- The old Jenkins apt signing key (2023) expired, which caused a `NO_PUBKEY` error during `apt update`; downloading the new `jenkins.io-2026.key` fixed it.
- Jenkins listens on port 8080; initial admin password is at `/var/lib/jenkins/secrets/initialAdminPassword`.

## Q5 - Version control with Git
- `git init` creates the `.git` folder; staging with `git add` moves files to the index.
- Working on a `feature/unit-tests` branch kept main stable while tests were written, and the fast-forward merge kept history linear.
- Tags (v1.0.0) are useful to mark working versions before the pipeline exists.

## Q6 - Basic Jenkins CI pipeline
- Creating the pipeline job with "Pipeline script from SCM" means Jenkins reads the Jenkinsfile from GitHub on every build, so pipeline changes are version controlled like code.
- The first build pulled the repo, ran all stages and archived the artifact (`app-build-1.tar.gz`) in ~29 seconds.

## Q7 - Jenkinsfile pipeline stages
- Declarative pipeline stages map cleanly to the CI/CD flow: Checkout -> Build -> Test -> Package -> Deploy.
- The Stage graph view in Jenkins shows each stage green, which makes failures easy to locate.
- `post { success / failure }` blocks give clear end-of-build messages in the console.

## Q3 - Automated deployment
- Poll SCM (`H/5 * * * *`) makes Jenkins check GitHub every ~5 minutes for new commits; a push triggers a build automatically without manual "Build Now".
- The deploy step copies the app to `/opt/devops-lab1`, creates a venv there, and restarts the systemd service with passwordless sudo (limited to the deploy script only via `/etc/sudoers.d/jenkins-deploy`).
- The health check (`curl /health` returning HTTP 200) inside deploy.sh turns the pipeline red immediately if the app does not come back up.

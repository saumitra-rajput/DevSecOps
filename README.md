#  DevSecOps — Pipeline [![DevSecOps End to End Pipeline](https://github.com/saumitra-rajput/DevSecOps/actions/workflows/devsecops-pipeline.yml/badge.svg)](https://github.com/saumitra-rajput/DevSecOps/actions/workflows/devsecops-pipeline.yml)

A fully automated CI/CD DevSecOps pipeline built with **GitHub Actions**, **Docker**, **Docker Hub**, and **AWS EC2**. Every commit triggers a chain of security scans, tests, image builds, and automated deployment to production on **port 80**.

---

## 📁 Project Structure :shipit: 

```
.
├── .github/
│   └── workflows/
│       ├── devsecops-pipeline.yml   # Master orchestrator workflow
│       ├── code-quality.yml         # Flake8 + Bandit (matrix strategy)
│       ├── secrets-scan.yml         # Gitleaks
│       ├── dependency-scan.yml      # pip-audit
│       ├── docker-scan.yml          # Hadolint
│       ├── test-run.yml             # Pytest
│       ├── build-push.yml           # Docker build & push to Docker Hub (SHA tag)
│       ├── image-scan.yml           # Trivy
│       └── deploy.yml               # Deploy to AWS EC2 (port 80)
├── templates/
│   └── index.html                   # Batman-themed pipeline dashboard
├── .flake8                          # max-line-length = 120
├── .trivyignore                     # CVE-2026-08661
├── app.py                           # Flask application
├── docker-compose.yml               # Docker Compose v2 config
├── Dockerfile                       # Container definition
├── LICENSE
├── requirements.txt                 # Python dependencies
└── test_app.py                      # Pytest test suite
```

---

## ⚙️ Pipeline Overview

The master workflow `devsecops-pipeline.yml` orchestrates all stages in sequence via `workflow_call`. Each stage must pass before the next begins.

```
Code Quality
     ↓
Secrets Scan
     ↓
Dependency Scan
     ↓
Docker Scan
     ↓
Test Run
     ↓
Build & Push  ──→  (SHA-tagged image pushed to Docker Hub)
     ↓
Image Scan
     ↓
Deploy  ──→  AWS EC2 : port 80
```

### Stage Breakdown

| # | Workflow | Tool | Description |
|---|----------|------|-------------|
| 1 | `code-quality.yml` | Flake8 + Bandit | Linting & static security analysis on Python 3.10, 3.11, 3.12 using matrix strategy |
| 2 | `secrets-scan.yml` | Gitleaks | Scans repository history for hardcoded secrets and credentials |
| 3 | `dependency-scan.yml` | pip-audit | Audits Python dependencies against known CVE database |
| 4 | `docker-scan.yml` | Hadolint | Lints the Dockerfile against Docker best practices |
| 5 | `test-run.yml` | Pytest | Runs the Flask application test suite |
| 6 | `build-push.yml` | Docker | Builds image from Dockerfile and pushes to Docker Hub tagged with Git SHA |
| 7 | `image-scan.yml` | Trivy | Scans the pushed container image for OS and library vulnerabilities |
| 8 | `deploy.yml` | SSH + Docker Compose v2 | Deploys SHA-tagged image to AWS EC2, runs container on port 80 |

---

## 🔐 GitHub Actions Configuration

Go to your repository → **Settings** → **Secrets and variables** → **Actions** to add the following.

### Variables
| Variable | Value |
|----------|-------|
| `DOCKERHUB_USER` | Your Docker Hub username |

### Secrets
| Secret | Description |
|--------|-------------|
| `DOCKERHUB_SECRET` | Docker Hub access token or password |
| `EC2_HOST` | Public IP address or hostname of your AWS EC2 instance |
| `EC2_USER` | SSH login username (e.g. `ubuntu`) |
| `EC2_SSH_KEY` | Private SSH key for EC2 access (full PEM contents) |

---

## 🐳 Docker Image Tagging

Images are built from the `Dockerfile` and tagged with the **Git commit SHA** in `build-push.yml`:

```
docker.io/<DOCKERHUB_USER>/<image-name>:<github.sha>
```

The same SHA is passed as an output from `build-push.yml` into `image-scan.yml` and `deploy.yml`, guaranteeing the exact image that was scanned is the one running in production.

---

## 🚀 Deploy Stage

`deploy.yml` SSHs into the AWS EC2 instance and runs the following steps in order:

1. Install required packages on the server
2. Log in to `docker.io` using `DOCKERHUB_USER` and `DOCKERHUB_SECRET`
3. Pull the specific SHA-tagged image from Docker Hub
4. Build and start the container using **Docker Compose v2** (`docker compose up`)
5. Container is exposed on **port 80**

---

## 🧪 Running Locally

### Prerequisites
- Python 3.10+
- Docker & Docker Compose v2
- pip

### Install & Run

```bash
# Clone the repo
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
# Visit http://localhost:5000
```

### Run Tests

```bash
pytest test_app.py -v
```

### Run with Docker Compose

```bash
docker compose up --build
# Visit http://localhost:80
```

---

## 🛡️ Security Configuration

### `.flake8`
```ini
[flake8]
max-line-length = 120
```

### `.trivyignore`
```
CVE-2026-08661
```
Trivy will skip this CVE during the image scan stage.

---

## 📦 `requirements.txt`

```
flask>=2.0.0
flake8
pytest
bandit
```

---

## 🛠️ Tools & Integrations

| Tool | Purpose |
|------|---------|
| **GitHub** | Source control & workflow triggers |
| **GitHub Actions** | CI/CD pipeline orchestration |
| **Docker** | Containerisation & image build |
| **Docker Hub (`docker.io`)** | Container image registry |
| **AWS EC2** | Production server (port 80) |

---

## 📄 License

See [LICENSE](./LICENSE) for details.
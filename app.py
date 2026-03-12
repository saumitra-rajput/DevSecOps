from flask import Flask, render_template, jsonify


app = Flask(__name__)


PIPELINE_DATA = {
    "project": "DevSecOps",
    "theme": "Batman CI/CD Pipeline",
    "stages": [
        {
            "id": "code-quality",
            "name": "Code Quality",
            "icon": "🔍",
            "strategy": "matrix",
            "python_versions": ["3.10", "3.11", "3.12"],
            "jobs": [
                {"name": "flake8", "desc": "PEP8 linting & style enforcement"},
                {"name": "bandit", "desc": "Security vulnerability static analysis"}
            ],
            "status": "success",
            "duration": "45s"
        },
        {
            "id": "secrets-scan",
            "name": "Secrets Scan",
            "icon": "🔐",
            "strategy": "single",
            "jobs": [
                {"name": "gitleaks", "desc": "Detect hardcoded secrets & credentials"}
            ],
            "status": "success",
            "duration": "7s"
        },
        {
            "id": "dependency-scan",
            "name": "Dependency Scan",
            "icon": "📦",
            "strategy": "single",
            "jobs": [
                {"name": "pip-audit", "desc": "CVE scan on Python dependencies"}
            ],
            "status": "success",
            "duration": "21s"
        },
        {
            "id": "docker-scan",
            "name": "Docker Scan",
            "icon": "🐳",
            "strategy": "single",
            "jobs": [
                {"name": "hadolint", "desc": "Dockerfile best practices linter"}
            ],
            "status": "success",
            "duration": "10s"
        },
        {
            "id": "test-run",
            "name": "Test Run",
            "icon": "🧪",
            "strategy": "single",
            "jobs": [
                {"name": "pytest", "desc": "Flask application unit & integration tests"}
            ],
            "status": "success",
            "duration": "10s"
        },
        {
            "id": "build-push",
            "name": "Build & Push",
            "icon": "🏗️",
            "strategy": "single",
            "jobs": [
                {"name": "docker-build", "desc": "Build Docker image"},
                {"name": "docker-push", "desc": "Push to Docker Hub with SHA tag"}
            ],
            "status": "success",
            "duration": "31s"
        },
        {
            "id": "image-scan",
            "name": "Image Scan",
            "icon": "🛡️",
            "strategy": "single",
            "jobs": [
                {"name": "trivy", "desc": "Container image vulnerability scanner"}
            ],
            "status": "success",
            "duration": "17s"
        },
        {
            "id": "deploy",
            "name": "Deploy",
            "icon": "🚀",
            "strategy": "single",
            "jobs": [
                {"name": "ssh-login", "desc": "SSH into AWS EC2 production server"},
                {"name": "install-deps", "desc": "Install required packages"},
                {"name": "docker-login", "desc": "Authenticate with Docker Hub"},
                {"name": "pull-image", "desc": "Pull specific SHA-tagged image"},
                {"name": "docker-compose", "desc": "Build & run container via Docker Compose"}
            ],
            "status": "success",
            "duration": "23s"
        }
    ],
    "tools": [
        {"name": "GitHub Actions", "icon": "⚙️"},
        {"name": "Docker Hub", "icon": "🐳"},
        {"name": "AWS EC2", "icon": "☁️"},
        {"name": "GitHub", "icon": "🐙"},
        {"name": "Docker", "icon": "📦"}
    ]
}


@app.route("/")
def index():
    return render_template("index.html", pipeline=PIPELINE_DATA)


@app.route("/api/pipeline")
def api_pipeline():
    return jsonify(PIPELINE_DATA)


@app.route("/api/status")
def api_status():
    stages = []
    for stage in PIPELINE_DATA["stages"]:
        stages.append({
            "id": stage["id"],
            "name": stage["name"],
            "status": stage["status"],
            "duration": stage["duration"]
        })
    return jsonify({"stages": stages, "overall": "success"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)  # nosec B104

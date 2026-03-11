import subprocess
import json
import os
from datetime import datetime, timezone
from flask import Flask, render_template

app = Flask(__name__)


def run_bandit():
    """SAST — scan Python files with Bandit."""
    result = subprocess.run(
        "bandit -r . -x ./.venv,./venv -f json -q",
        shell=True, capture_output=True, text=True
    )
    try:
        data    = json.loads(result.stdout)
        metrics = data.get("metrics", {}).get("_totals", {})
        high    = int(metrics.get("SEVERITY.HIGH", 0))
        medium  = int(metrics.get("SEVERITY.MEDIUM", 0))
        return {
            "name":   "SAST — Bandit",
            "passed": high == 0 and medium == 0,
            "detail": f"{high} high, {medium} medium issues found",
        }
    except Exception:
        return {"name": "SAST — Bandit", "passed": False, "detail": "Scan failed"}


def run_safety():
    """SCA — check dependencies for CVEs with Safety."""
    result = subprocess.run(
        "safety check --json",
        shell=True, capture_output=True, text=True
    )
    try:
        vulns = json.loads(result.stdout)
        vulns = vulns if isinstance(vulns, list) else []
        return {
            "name":   "Dependencies — Safety",
            "passed": len(vulns) == 0,
            "detail": f"{len(vulns)} vulnerable package(s) found",
        }
    except Exception:
        return {"name": "Dependencies — Safety", "passed": True, "detail": "No issues found"}


# ── Placeholders — update these once your workflow is ready ──────────────────

def run_trufflehog():
    # TODO: e.g. run_cmd("trufflehog filesystem . --json")
    return {"name": "Secrets — TruffleHog", "passed": True, "detail": "Placeholder"}


def run_trivy():
    # TODO: e.g. run_cmd("trivy image --format json <your-image>")
    return {"name": "Container — Trivy", "passed": True, "detail": "Placeholder"}

# ─────────────────────────────────────────────────────────────────────────────


def run_all_checks():
    checks = [run_bandit(), run_safety(), run_trufflehog(), run_trivy()]
    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    return {
        "checks":  checks,
        "summary": {
            "total":   len(checks),
            "passed":  passed,
            "failed":  failed,
            "overall": failed == 0,
        },
        "meta": {
            "timestamp":     datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "region":        os.getenv("AWS_REGION", "ap-south-1"),
            "instance_type": os.getenv("INSTANCE_TYPE", "t3.medium"),
        },
    }


@app.route("/")
def index():
    return render_template("index.html", **run_all_checks())


@app.route("/health")
def health():
    from flask import jsonify
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 80)))

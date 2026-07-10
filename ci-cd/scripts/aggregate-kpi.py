#!/usr/bin/env python3
import json, os, glob
from datetime import datetime

METRICS_FILE = "kpi-metrics.json"
PROM_FILE = "/tmp/ebc-kpi.prom"

def safe_read_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def aggregate_kpis():
    kpis = {
        "timestamp": datetime.now().isoformat(),
        "project": "EBC Security Testing Platform",
        "version": "1.0.0",
        "kpis": {}
    }

    # SonarQube
    sonar = safe_read_json("sonar-report.json")
    if sonar:
        issues = sonar.get("issues", [])
        kpis["kpis"]["sonarqube"] = {
            "total_issues": len(issues),
            "critical": len([i for i in issues if i.get("severity") == "CRITICAL"]),
            "major": len([i for i in issues if i.get("severity") == "MAJOR"]),
            "status": "PASSED" if len([i for i in issues if i.get("severity") in ("CRITICAL","MAJOR")]) < 10 else "FAILED"
        }
    else:
        kpis["kpis"]["sonarqube"] = {"status": "NO_DATA"}

    # Trivy (image and fs)
    trivy_data = None
    for f in glob.glob("trivy-*.json"):
        trivy_data = safe_read_json(f)
        if trivy_data:
            break
    if trivy_data:
        results = trivy_data.get("Results", [])
        total_vulns = sum(len(r.get("Vulnerabilities", [])) for r in results)
        critical = sum(len([v for v in r.get("Vulnerabilities", []) if v.get("Severity") == "CRITICAL"]) for r in results)
        high = sum(len([v for v in r.get("Vulnerabilities", []) if v.get("Severity") == "HIGH"]) for r in results)
        kpis["kpis"]["trivy"] = {"total_vulnerabilities": total_vulns, "critical": critical, "high": high, "status": "PASSED" if critical == 0 else "FAILED"}
    else:
        kpis["kpis"]["trivy"] = {"status": "NO_DATA"}

    # Gitleaks
    gitleaks = safe_read_json("gitleaks-report.json")
    if gitleaks:
        count = len(gitleaks) if isinstance(gitleaks, list) else 0
        kpis["kpis"]["gitleaks"] = {"secrets_found": count, "status": "PASSED" if count == 0 else "FAILED"}
    else:
        kpis["kpis"]["gitleaks"] = {"status": "NO_DATA"}

    # ZAP
    zap = safe_read_json("zap-report.json")
    if zap:
        alerts = zap.get("site", [{}])[0].get("alerts", [])
        high = len([a for a in alerts if a.get("riskcode") == "3"])
        medium = len([a for a in alerts if a.get("riskcode") == "2"])
        kpis["kpis"]["zap"] = {"high_alerts": high, "medium_alerts": medium, "total_alerts": len(alerts), "status": "PASSED" if high == 0 else "FAILED"}
    else:
        kpis["kpis"]["zap"] = {"status": "NO_DATA"}

    # Global score
    scores = []
    for tool, data in kpis["kpis"].items():
        if data.get("status") == "PASSED":
            scores.append(100)
        elif data.get("status") == "FAILED":
            scores.append(0)
        else:
            scores.append(50)
    kpis["global_score"] = round(sum(scores) / len(scores), 2) if scores else 0
    kpis["overall_status"] = "PASSED" if kpis["global_score"] >= 80 else "NEEDS_IMPROVEMENT"

    with open(METRICS_FILE, "w") as f:
        json.dump(kpis, f, indent=2)

    # Write Prometheus metric file
    ts = int(datetime.now().timestamp())
    with open(PROM_FILE, "w") as f:
        f.write("# HELP ebc_security_score Global security score\n")
        f.write("# TYPE ebc_security_score gauge\n")
        f.write(f"ebc_security_score {kpis['global_score']} {ts}\n")
        for tool, data in kpis["kpis"].items():
            f.write(f"# HELP ebc_{tool}_status {tool} status (1=PASSED, 0=FAILED, 0.5=NO_DATA)\n")
            f.write(f"# TYPE ebc_{tool}_status gauge\n")
            val = 1 if data.get("status") == "PASSED" else (0 if data.get("status") == "FAILED" else 0.5)
            f.write(f"ebc_{tool}_status {val} {ts}\n")

    print(json.dumps(kpis, indent=2))
    print(f"\nScore global: {kpis['global_score']}% - {kpis['overall_status']}")
    print(f"Prometheus metrics written to {PROM_FILE}")
    return kpis

if __name__ == "__main__":
    aggregate_kpis()

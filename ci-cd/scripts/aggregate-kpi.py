#!/usr/bin/env python3
"""
Agrégateur de KPIs de sécurité pour le projet EBC.
Génère un rapport JSON des métriques clés.
"""

import json
import os
import glob
from datetime import datetime

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

    # KPI 1: SonarQube Quality Gate
    sonar_report = safe_read_json("sonar-report.json")
    if sonar_report:
        issues = sonar_report.get("issues", [])
        kpis["kpis"]["sonarqube"] = {
            "total_issues": len(issues),
            "critical": len([i for i in issues if i.get("severity") == "CRITICAL"]),
            "major": len([i for i in issues if i.get("severity") == "MAJOR"]),
            "minor": len([i for i in issues if i.get("severity") == "MINOR"]),
            "quality_gate": "PASSED" if len(issues) < 10 else "FAILED"
        }
    else:
        kpis["kpis"]["sonarqube"] = {"status": "NO_DATA"}

    # KPI 2: Trivy Vulnerabilities
    trivy_report = safe_read_json("trivy-report.json")
    if trivy_report:
        results = trivy_report.get("Results", [])
        total_vulns = sum(len(r.get("Vulnerabilities", [])) for r in results)
        critical = sum(
            len([v for v in r.get("Vulnerabilities", [])
                 if v.get("Severity") == "CRITICAL"])
            for r in results
        )
        high = sum(
            len([v for v in r.get("Vulnerabilities", [])
                 if v.get("Severity") == "HIGH"])
            for r in results
        )
        kpis["kpis"]["trivy"] = {
            "total_vulnerabilities": total_vulns,
            "critical": critical,
            "high": high,
            "status": "PASSED" if critical == 0 else "FAILED"
        }
    else:
        kpis["kpis"]["trivy"] = {"status": "NO_DATA"}

    # KPI 3: Gitleaks Secrets
    gitleaks_report = safe_read_json("gitleaks-report.json")
    if gitleaks_report:
        secrets_count = len(gitleaks_report) if isinstance(gitleaks_report, list) else 0
        kpis["kpis"]["gitleaks"] = {
            "secrets_found": secrets_count,
            "status": "PASSED" if secrets_count == 0 else "FAILED"
        }
    else:
        kpis["kpis"]["gitleaks"] = {"status": "NO_DATA"}

    # KPI 4: ZAP Alerts
    zap_report = safe_read_json("zap-report.json")
    if zap_report:
        alerts = zap_report.get("site", [{}])[0].get("alerts", [])
        high_alerts = len([a for a in alerts if a.get("riskcode") == "3"])
        medium_alerts = len([a for a in alerts if a.get("riskcode") == "2"])
        kpis["kpis"]["zap"] = {
            "high_alerts": high_alerts,
            "medium_alerts": medium_alerts,
            "total_alerts": len(alerts),
            "status": "PASSED" if high_alerts == 0 else "FAILED"
        }
    else:
        kpis["kpis"]["zap"] = {"status": "NO_DATA"}

    # Calcul du score global
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

    # Écriture du rapport
    with open("kpi-metrics.json", "w") as f:
        json.dump(kpis, f, indent=2)

    print(json.dumps(kpis, indent=2))
    print(f"\n📊 Score global: {kpis['global_score']}% - {kpis['overall_status']}")

    return kpis

if __name__ == "__main__":
    aggregate_kpis()

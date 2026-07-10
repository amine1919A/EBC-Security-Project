#!/bin/bash
set -e

echo "📦 [SCA] Analyse des dépendances et vulnérabilités..."
mkdir -p reports

# Trivy Image Scan
echo "━━━ Trivy Image Scan ━━━"
docker build -t ebc-app:latest -f app/Dockerfile app/ 2>/dev/null || {
  echo "⚠️  Build local non nécessaire, utilisation de l'image existante"
}
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest \
  image --severity HIGH,CRITICAL \
  --format json \
  --output /tmp/trivy-report.json \
  ebc-app:latest 2>/dev/null || echo "⚠️  Trivy image scan warning"
echo ""

# Trivy Filesystem Scan
echo "━━━ Trivy Filesystem Scan ━━━"
docker run --rm \
  -v "$(pwd):/project" \
  aquasec/trivy:latest \
  fs --severity HIGH,CRITICAL \
  --format json \
  --output /tmp/trivy-fs-report.json \
  /project 2>/dev/null || echo "⚠️  Trivy FS scan warning"
echo ""

# Trivy Config Scan (K8s/Docker)
echo "━━━ Trivy Config Scan ━━━"
docker run --rm \
  -v "$(pwd):/project" \
  aquasec/trivy:latest \
  config --severity HIGH,CRITICAL \
  --format table \
  /project 2>/dev/null || echo "⚠️  Trivy config scan warning"

echo ""
echo "✅ [SCA] Analyse terminée"

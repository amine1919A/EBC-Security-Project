#!/bin/bash
set -e

echo "🌐 [DAST] Lancement des tests dynamiques..."
TARGET_URL=${1:-http://app:80}
echo "   Cible: $TARGET_URL"
echo ""

# ZAP Baseline Scan
echo "━━━ OWASP ZAP Baseline Scan ━━━"
docker run --rm \
  --network ebc-network \
  -v "$(pwd)/security-tools/owasp-zap/policies:/zap/policies" \
  -v "$(pwd)/reports:/zap/reports" \
  owasp/zap2docker-stable \
  zap-baseline.py \
    -t "$TARGET_URL" \
    -r /zap/reports/zap-report.html \
    -c /zap/policies/EBC-policy.policy \
    -I || echo "⚠️  ZAP a trouvé des alertes (voir rapport)"

echo ""

# Nikto Scan
echo "━━━ Nikto Scan ━━━"
docker run --rm \
  --network ebc-network \
  -v "$(pwd)/reports:/reports" \
  alpine:latest \
  sh -c "apk add --no-cache nikto && \
         nikto -h $TARGET_URL -Format xml \
         -output /reports/nikto-report.xml \
         -Tuning 123456789" || echo "⚠️  Nikto terminé"

echo ""
echo "✅ [DAST] Tests dynamiques terminés"
echo "   Rapport ZAP:   reports/zap-report.html"
echo "   Rapport Nikto: reports/nikto-report.xml"

#!/bin/bash
set -e

echo "🔍 [SAST] Lancement de l'analyse statique..."
echo ""

# SonarQube Scan
echo "━━━ SonarQube Scan ━━━"
docker run --rm \
  --network ebc-network \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli \
  sonar-scanner \
    -Dsonar.projectKey=ebc-app \
    -Dsonar.host.url=http://sonarqube:9000 \
    -Dsonar.login=${SONAR_TOKEN:-admin} \
    -Dsonar.sources=/usr/src \
    -Dsonar.exclusions=vendor/**,node_modules/**,var/** \
    -Dsonar.php.coverage.reportPaths=coverage.xml \
    -Dsonar.qualitygate.wait=true || echo "⚠️  SonarQube warning (non-bloquant)"

echo ""

# PHPStan Scan
echo "━━━ PHPStan Scan ━━━"
if [ -f app/symfony/vendor/bin/phpstan ]; then
  cd app/symfony
  vendor/bin/phpstan analyse --level=max src/ \
    --error-format=table || echo "⚠️  PHPStan warnings"
  cd ../..
else
  echo "⚠️  PHPStan non installé, exécution de composer install..."
  cd app/symfony
  composer install --no-interaction --no-progress 2>/dev/null || true
  vendor/bin/phpstan analyse --level=max src/ \
    --error-format=table || echo "⚠️  PHPStan warnings"
  cd ../..
fi

echo ""
echo "✅ [SAST] Analyse terminée"

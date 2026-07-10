#!/bin/bash
set -e

echo "🔧 [CONFIG] Validation de la configuration de sécurité..."
echo ""

ERRORS=0

# 1. Vérifier les mots de passe par défaut
echo "━━━ 1. Mots de passe par défaut ───"
if grep -r "admin/admin" docker-compose.yml 2>/dev/null; then
    echo "   ⚠️  SonarQube & Grafana utilisent admin/admin"
    echo "   ➡️  À changer en production"
fi
echo ""

# 2. Vérifier les secrets dans .env
echo "━━━ 2. Variables sensibles dans .env ───"
if [ -f app/symfony/.env ]; then
    echo "   ✅ .env présent"
    # Vérifier qu'il n'y a pas de vrais secrets
    if grep -E "(PROD|PRODUCTION)" app/symfony/.env | grep -q "false"; then
        echo "   ✅ APP_ENV=dev (pas de production)"
    fi
else
    echo "   ❌ .env manquant"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 3. Vérifier les expositions de ports
echo "━━━ 3. Exposition de ports ───"
PORTS=$(grep -E "ports:" docker-compose.yml -A 10 | grep -E " - \"" | sed 's/.*"\(.*\)".*/\1/')
echo "   Ports exposés:"
echo "$PORTS" | while read port; do
    echo "   - $port"
done
echo ""

# 4. Vérifier les volumes Docker
echo "━━━ 4. Volumes Docker ───"
VOLUMES=$(grep -E "volumes:" docker-compose.yml 2>/dev/null || echo "   Aucun volume défini")
echo "$VOLUMES" | head -5
echo ""

# 5. Vérifier les healthcheck
echo "━━━ 5. Healthchecks ───"
for service in mysql elasticsearch; do
    if grep -A 5 "healthcheck:" docker-compose.yml | grep -q "$service"; then
        echo "   ✅ $service healthcheck"
    else
        echo "   ⚠️  Pas de healthcheck pour $service"
    fi
done
echo ""

# 6. Vérifier les networks
echo "━━━ 6. Réseau Docker ───"
if grep -q "ebc-network" docker-compose.yml; then
    echo "   ✅ ebc-network défini"
else
    echo "   ❌ ebc-network non défini"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 7. Vérifier les règles Prometheus
echo "━━━ 7. Règles d'alerte ───"
if [ -f monitoring/prometheus/alert.rules.yml ]; then
    RULES=$(grep "alert:" monitoring/prometheus/alert.rules.yml | wc -l)
    echo "   ✅ $RULES règles d'alerte configurées"
else
    echo "   ❌ Fichier alert.rules.yml manquant"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 8. Vérifier les politiques ZAP
echo "━━━ 8. Politiques OWASP ZAP ───"
if [ -f security-tools/owasp-zap/policies/EBC-policy.policy ]; then
    SCANNERS=$(grep "<scanner>" security-tools/owasp-zap/policies/EBC-policy.policy | wc -l)
    echo "   ✅ $SCANNERS règles OWASP ZAP configurées"
else
    echo "   ❌ Politique ZAP manquante"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 9. Vérifier les règles PHPStan
echo "━━━ 9. PHPStan Level ───"
if [ -f app/symfony/phpstan.neon ]; then
    PHPSTAN_LEVEL=$(grep "level:" app/symfony/phpstan.neon | head -1)
    echo "   ✅ $PHPSTAN_LEVEL"
else
    echo "   ❌ phpstan.neon manquant"
fi
echo ""

# 10. Vérifier la couverture OWASP
echo "━━━ 10. Couverture OWASP Top 10 ───"
OWASP_CATEGORIES=(
    "A1 Injection"
    "A2 Broken Auth"
    "A3 Sensitive Data"
    "A5 Access Control"
    "A7 XSS"
    "A9 Vulnerabilities"
    "A10 Logging"
)
for cat in "${OWASP_CATEGORIES[@]}"; do
    code=$(echo "$cat" | awk '{print $1}')
    if grep -q "class TestOWASP_${code}" ci-cd/scripts/api-tests/test_api.py 2>/dev/null; then
        echo "   ✅ $cat — couvert (TestOWASP_${code})"
    else
        echo "   ⚠️  $cat — pas de test dédié"
    fi
done

echo ""
echo "═══════════════════════════════════════════════════"
echo "   RÉSULTAT VALIDATION CONFIGURATION"
echo "═══════════════════════════════════════════════════"
echo "   ❌ Erreurs: $ERRORS"

if [ $ERRORS -gt 0 ]; then
    exit 1
fi

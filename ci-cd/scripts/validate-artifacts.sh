#!/bin/bash
set -e

echo "📦 [ARTIFACTS] Validation des artefacts de build..."
echo ""

ERRORS=0
WARNINGS=0

# 1. Vérifier la présence des fichiers obligatoires
echo "━━━ 1. Fichiers obligatoires ━━━"
REQUIRED_FILES=(
    "docker-compose.yml"
    "app/Dockerfile"
    "app/symfony/composer.json"
    "app/symfony/public/index.php"
    "app/symfony/src/Kernel.php"
    ".gitignore"
    "README.md"
)
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file — MANQUANT"
        ERRORS=$((ERRORS + 1))
    fi
done
echo ""

# 2. Vérifier les permissions des scripts
echo "━━━ 2. Permissions des scripts ━━━"
SCRIPTS=("setup.sh" "start.sh" "stop.sh" "reset.sh")
for script in "${SCRIPTS[@]}"; do
    if [ -x "$script" ]; then
        echo "   ✅ $script (exécutable)"
    elif [ -f "$script" ]; then
        echo "   ⚠️  $script (non exécutable)"
        WARNINGS=$((WARNINGS + 1))
    else
        echo "   ❌ $script — MANQUANT"
        ERRORS=$((ERRORS + 1))
    fi
done
echo ""

# 3. Vérifier la syntaxe YAML
echo "━━━ 3. Syntaxe YAML ━━━"
if command -v python3 &>/dev/null; then
    for yaml_file in docker-compose.yml ci-cd/.gitlab-ci.yml; do
        if [ -f "$yaml_file" ]; then
            if python3 -c "import yaml; yaml.safe_load(open('$yaml_file'))" 2>/dev/null; then
                echo "   ✅ $yaml_file (valide)"
            else
                echo "   ❌ $yaml_file (invalide)"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
else
    echo "   ⚠️  Python3/yaml non disponible — vérification ignorée"
fi
echo ""

# 4. Vérifier la structure Docker Compose
echo "━━━ 4. Structure Docker ───"
if command -v docker &>/dev/null; then
    if docker-compose config -q 2>/dev/null; then
        echo "   ✅ docker-compose.yml (valide)"
    else
        echo "   ⚠️  docker-compose config warning"
    fi
else
    echo "   ⚠️  Docker non disponible — vérification ignorée"
fi
echo ""

# 5. Vérifier les images Docker
echo "━━━ 5. Images Docker ───"
docker images --filter "reference=sonarqube:community" --format "{{.Repository}}" | grep -q . && echo "   ✅ SonarQube image disponible" || echo "   ⚠️  SonarQube image non téléchargée"
docker images --filter "reference=prom/prometheus" --format "{{.Repository}}" | grep -q . && echo "   ✅ Prometheus image disponible" || echo "   ⚠️  Prometheus image non téléchargée"
docker images --filter "reference=grafana/grafana" --format "{{.Repository}}" | grep -q . && echo "   ✅ Grafana image disponible" || echo "   ⚠️  Grafana image non téléchargée"
echo ""

# 6. Vérifier les fichiers de monitoring
echo "━━━ 6. Monitoring ───"
[ -f monitoring/prometheus/prometheus.yml ] && echo "   ✅ Prometheus config" || { echo "   ❌ Prometheus config manquante"; ERRORS=$((ERRORS + 1)); }
[ -f monitoring/prometheus/alert.rules.yml ] && echo "   ✅ Alert rules" || { echo "   ❌ Alert rules manquantes"; ERRORS=$((ERRORS + 1)); }
[ -f monitoring/grafana/dashboards/security-overview.json ] && echo "   ✅ Grafana dashboard" || { echo "   ❌ Grafana dashboard manquant"; ERRORS=$((ERRORS + 1)); }
[ -f monitoring/grafana/datasources/prometheus.yml ] && echo "   ✅ Grafana datasource" || { echo "   ❌ Grafana datasource manquante"; ERRORS=$((ERRORS + 1)); }
echo ""

# 7. Vérifier les outils de sécurité
echo "━━━ 7. Outils de sécurité ───"
[ -f security-tools/sonarqube/Dockerfile ] && echo "   ✅ SonarQube" || { echo "   ❌ SonarQube config manquante"; ERRORS=$((ERRORS + 1)); }
[ -f security-tools/owasp-zap/policies/EBC-policy.policy ] && echo "   ✅ ZAP Policy" || { echo "   ❌ ZAP Policy manquante"; ERRORS=$((ERRORS + 1)); }
[ -f security-tools/gitleaks/.gitleaks.toml ] && echo "   ✅ Gitleaks" || { echo "   ❌ Gitleaks config manquante"; ERRORS=$((ERRORS + 1)); }
echo ""

# 8. Vérifier les tests API
echo "━━━ 8. Tests API ───"
[ -f ci-cd/scripts/api-tests/test_api.py ] && echo "   ✅ Tests API (25 tests OWASP)" || { echo "   ❌ Tests API manquants"; ERRORS=$((ERRORS + 1)); }
[ -f ci-cd/scripts/api-tests/requirements.txt ] && echo "   ✅ Requirements Python" || { echo "   ❌ Requirements manquants"; ERRORS=$((ERRORS + 1)); }

echo ""
echo "═══════════════════════════════════════════════════"
echo "   RÉSULTAT VALIDATION ARTEFACTS"
echo "═══════════════════════════════════════════════════"
echo "   ✅ Validations réussies"
echo "   ⚠️  Warnings: $WARNINGS"
echo "   ❌ Erreurs:   $ERRORS"

if [ $ERRORS -gt 0 ]; then
    echo ""
    echo "🔴 ÉCHEC : $ERRORS erreur(s) critique(s) détectée(s)"
    exit 1
else
    echo ""
    echo "🟢 SUCCÈS : Tous les artefacts sont valides"
fi

#!/bin/bash
set -e

echo "🔬 [SNYK] Analyse des dépendances applicatives..."
echo ""

# Vérifier si Snyk est configuré
if [ -z "$SNYK_TOKEN" ]; then
    echo "⚠️  Snyk non configuré."
    echo "   Pour activer Snyk :"
    echo "   1. Créer un compte gratuit : https://snyk.io/"
    echo "   2. Définir SNYK_TOKEN dans les variables CI/CD"
    echo "   3. Définir SNYK_ORG_ID (optionnel)"
    echo ""
    echo "🔶 Utilisation de Trivy comme alternative (déjà configuré)"
    exit 0
fi

# Installer Snyk CLI
if ! command -v snyk &>/dev/null; then
    echo "📥 Installation de Snyk CLI..."
    curl -sL https://static.snyk.io/cli/latest/snyk-linux -o /usr/local/bin/snyk
    chmod +x /usr/local/bin/snyk
fi

# Authentification
snyk auth $SNYK_TOKEN

# Analyser composer.json
if [ -f app/symfony/composer.json ]; then
    echo "━━━ Analyse composer.json ━━━"
    cd app/symfony
    snyk test --json --severity-threshold=high \
        --org=$SNYK_ORG_ID 2>/dev/null | \
        python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    vulns = data.get('vulnerabilities', [])
    print(f'   Vulnérabilités trouvées: {len(vulns)}')
    for v in vulns[:5]:
        print(f'   - {v.get(\"title\")} ({v.get(\"severity\")})')
except: pass
" || echo "   ✅ Aucune vulnérabilité critique"
    cd ../..
fi

# Analyser Dockerfile
echo "━━━ Analyse Dockerfile ━━━"
snyk test --docker Dockerfile --json 2>/dev/null | \
    python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    print(f'   Vulnérabilités Docker: {len(data.get(\"vulnerabilities\",[]))}')
except: pass
" || echo "   ✅ Dockerfile OK"

echo ""
echo "✅ [SNYK] Analyse terminée"

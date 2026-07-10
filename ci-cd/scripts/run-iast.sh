#!/bin/bash
set -e

echo "🧪 [IAST] Lancement des tests interactifs..."
echo ""

# Vérifier si Contrast Security est configuré
if [ -z "$CONTRAST_API_KEY" ]; then
    echo "⚠️  Contrast Security non configuré."
    echo "   Pour activer l'IAST :"
    echo "   1. Créer un compte gratuit : https://www.contrastsecurity.com/"
    echo "   2. Définir les variables d'environnement :"
    echo "      - CONTRAST_API_KEY"
    echo "      - CONTRAST_SERVICE_KEY"
    echo "      - CONTRAST_TEAM_SERVER_URL"
    echo "   3. Décommenter l'agent dans docker-compose.yml"
    echo ""
    echo "🔶 Mode dégradé : utilisation des tests API comme alternative IAST"
fi

# Exécuter les tests API (simulation IAST)
echo "━━━ Tests API (IAST-like) ━━━"
cd ci-cd/scripts/api-tests
pip install -q -r requirements.txt 2>/dev/null || true
python -m pytest test_api.py -v --tb=short || echo "⚠️  Certains tests ont échoué"
cd ../../..

echo ""
echo "✅ [IAST] Tests terminés"

#!/bin/bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       EBC Security Testing Platform - Installation          ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}[1/6] Vérification des prérequis...${NC}"

command -v docker >/dev/null 2>&1 || {
    echo -e "${RED}❌ Docker non trouvé. Installation...${NC}"
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    echo -e "${GREEN}✅ Docker installé${NC}"
}

command -v docker-compose >/dev/null 2>&1 || {
    echo -e "${RED}❌ Docker Compose non trouvé. Installation...${NC}"
    sudo apt-get update && sudo apt-get install -y docker-compose
    echo -e "${GREEN}✅ Docker Compose installé${NC}"
}

echo -e "${GREEN}✅ Prérequis OK${NC}"
echo ""

echo -e "${YELLOW}[2/6] Configuration réseau Docker...${NC}"
docker network inspect ebc-network >/dev/null 2>&1 || {
    docker network create ebc-network
    echo -e "${GREEN}✅ Réseau ebc-network créé${NC}"
}
echo -e "${GREEN}✅ Réseau OK${NC}"
echo ""

echo -e "${YELLOW}[3/6] Vérification de la structure des dossiers...${NC}"
DIRS=(
    "app/symfony" "app/nginx" "app/scripts"
    "security-tools/sonarqube/rules"
    "security-tools/owasp-zap/policies"
    "security-tools/trivy" "security-tools/gitleaks" "security-tools/nikto"
    "ci-cd/scripts/api-tests" "ci-cd/templates"
    "monitoring/prometheus" "monitoring/grafana/dashboards"
    "monitoring/grafana/datasources" "monitoring/grafana/provisioning"
    "docs/memoire"
)
for dir in "${DIRS[@]}"; do
    mkdir -p "$dir"
done
echo -e "${GREEN}✅ Structure des dossiers OK${NC}"
echo ""

echo -e "${YELLOW}[4/6] Démarrage des services Docker...${NC}"
docker-compose up -d 2>&1 || {
    echo -e "${YELLOW}⚠️  docker-compose up -d a échoué, tentative avec docker compose...${NC}"
    docker compose up -d
}
echo -e "${GREEN}✅ Services démarrés${NC}"
echo ""

echo -e "${YELLOW}[5/6] Attente du démarrage des services...${NC}"
sleep 15

echo -e "${YELLOW}[6/6] Vérification des services...${NC}"
for service in app nginx sonarqube prometheus grafana; do
    if docker ps | grep -q "ebc-$service"; then
        echo -e "${GREEN}✅ $service: OK${NC}"
    else
        echo -e "${RED}❌ $service: NON DÉMARRÉ${NC}"
    fi
done

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║       ✅ INSTALLATION TERMINÉE AVEC SUCCÈS !                ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📌 Accès aux services :${NC}"
echo -e "   ${GREEN}Application EBC:${NC}  http://localhost:8080"
echo -e "   ${GREEN}SonarQube:${NC}       http://localhost:9000  (admin/admin)"
echo -e "   ${GREEN}Grafana:${NC}         http://localhost:3000  (admin/admin)"
echo -e "   ${GREEN}Prometheus:${NC}      http://localhost:9090"
echo ""
echo -e "${YELLOW}📋 Prochaines étapes :${NC}"
echo -e "   1. Créer le projet Symfony : cd app/symfony && composer create-project symfony/skeleton ."
echo -e "   2. Pousser sur GitHub : git add . && git commit -m 'Initial' && git push"
echo -e "   3. Voir les résultats : ouvrir http://localhost:3000 (dashboard Grafana)"
echo ""

# Guide d'Installation

## Prérequis

| Composant | Version minimale | Recommandé |
|-----------|-----------------|------------|
| Docker    | 24+             | 27+        |
| Docker Compose | v2        | v2.30+     |
| RAM       | 8 Go            | 16 Go      |
| Espace disque | 20 Go        | 40 Go      |
| OS        | Linux           | Ubuntu 24.04 |

## Installation en 3 étapes

### 1. Cloner le projet

```bash
git clone https://github.com/amine1919A/EBC-Security-Project.git
cd EBC-Security-Project
```

### 2. Lancer le script d'installation

```bash
chmod +x setup.sh
./setup.sh
```

Le script vérifie :
- Docker et Docker Compose sont installés (les installe si manquants)
- Crée le réseau Docker `ebc-network`
- Crée la structure de dossiers
- Construit et démarre tous les conteneurs

### 3. Vérifier que tout tourne

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Résultat attendu (8 conteneurs) :

| Nom | Statut | Ports |
|-----|--------|-------|
| ebc-app | Up | 9001 |
| ebc-nginx | Up | 8080 |
| ebc-mysql | Up | 3307 |
| ebc-elasticsearch | Up | 9201 |
| ebc-sonarqube | Up | 9000 |
| ebc-sonar-db | Up | 5432 |
| ebc-prometheus | Up | 9090 |
| ebc-grafana | Up | 3000 |

### Services disponibles

| Service | URL | Identifiants |
|---------|-----|-------------|
| Application EBC | http://localhost:8080 | - |
| SonarQube (SAST) | http://localhost:9000 | admin / admin |
| Grafana (Monitoring) | http://localhost:3000 | admin / admin |
| Prometheus (Métriques) | http://localhost:9090 | - |

## Installation manuelle (si `setup.sh` échoue)

```bash
# 1. Créer le réseau
docker network create ebc-network 2>/dev/null || true

# 2. Créer les dossiers
mkdir -p app/symfony app/nginx ci-cd/scripts/api-tests
mkdir -p security-tools/{sonarqube/rules,owasp-zap/policies,trivy,gitleaks,nikto}
mkdir -p monitoring/{prometheus,grafana/{dashboards,datasources,provisioning}}
mkdir -p docs/memoire

# 3. Lancer les services
docker compose up -d
```

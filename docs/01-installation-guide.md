# Guide d'Installation - EBC Security Testing Platform

## Prérequis

- Linux (Ubuntu 22.04+ recommandé)
- Docker 24+ et Docker Compose v2+
- Git
- 8 Go RAM minimum (16 Go recommandé)
- 20 Go espace disque libre

## Installation Rapide (PC Secondaire)

```bash
# 1. Cloner le dépôt
git clone https://github.com/amine1919A/EBC-Security-Project.git
cd EBC-Security-Project

# 2. Lancer l'installation one-click
chmod +x setup.sh
./setup.sh
```

## Installation Manuelle

```bash
# 1. Vérifier Docker
docker --version
docker-compose --version

# 2. Créer le réseau Docker
docker network create ebc-network

# 3. Démarrer les services
docker-compose up -d

# 4. Vérifier que tout tourne
docker ps

# 5. Accéder aux interfaces
# Application:  http://localhost:8080
# SonarQube:    http://localhost:9000 (admin/admin)
# Grafana:      http://localhost:3000 (admin/admin)
```

## Configuration Après Installation

### 1. SonarQube
1. Aller sur http://localhost:9000
2. Login: admin / admin
3. Changer le mot de passe
4. Créer un token: My Account → Security → Generate Token
5. Configurer la variable SONAR_TOKEN dans le CI/CD

### 2. Grafana
1. Aller sur http://localhost:3000
2. Login: admin / admin
3. Changer le mot de passe
4. Les dashboards sont pré-configurés

### 3. Application Symfony
```bash
cd app/symfony
composer create-project symfony/skeleton:"6.4.*" .
composer require api-platform/core
composer require --dev phpstan/phpstan
```

## Dépannage

### Ports déjà utilisés
```bash
# Modifier les ports dans docker-compose.yml
# Exemple: "8081:80" au lieu de "8080:80"
```

### Service ne démarre pas
```bash
# Voir les logs
docker logs ebc-sonarqube
docker logs ebc-app

# Redémarrer un service
docker restart ebc-app
```

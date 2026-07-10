# Guide de Dépannage - EBC Security Testing Platform

## 1. Problèmes Docker

### Service ne démarre pas
```bash
# Voir les logs détaillés
docker logs ebc-sonarqube --tail 100
docker logs ebc-app --tail 100
docker logs ebc-mysql --tail 100

# Vérifier les conteneurs en cours
docker ps -a

# Redémarrer un service spécifique
docker restart ebc-sonarqube

# Redémarrer tous les services
docker-compose restart
```

### Port déjà utilisé
```bash
# Vérifier quel processus utilise le port
sudo lsof -i :8080
sudo lsof -i :9000
sudo lsof -i :3000

# Modifier le port dans docker-compose.yml
# "8081:80" au lieu de "8080:80"
```

### Erreur "Cannot connect to Docker daemon"
```bash
# Démarrer Docker
sudo systemctl start docker
sudo systemctl enable docker

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER
# Déconnexion/reconnexion nécessaire
```

## 2. Problèmes CI/CD

### Pipeline échoue sur GitLab
```bash
# 1. Vérifier les logs du pipeline dans GitLab
# 2. Vérifier les variables CI/CD configurées
#    Settings → CI/CD → Variables
#    - SONAR_TOKEN
#    - SSH_PRIVATE_KEY
#    - DEPLOY_HOST
#    - DEPLOY_USER

# 3. Tester localement
docker run --rm -v $(pwd):/build gitlab/gitlab-runner exec docker test:api
```

### Runner GitLab ne trouve pas Docker
```yaml
# Dans .gitlab-ci.yml, ajouter :
variables:
  DOCKER_HOST: tcp://docker:2375
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: ""
```

## 3. Problèmes Outils de Sécurité

### SonarQube ne démarre pas
```bash
# Vérifier Elasticsearch (SonarQube en dépend)
# Solution : augmenter les ulimits
docker run --ulimit nofile=65536:65536 sonarqube:community

# Vérifier la mémoire
free -m  # Besoin d'au moins 2GB de libre
```

### ZAP ne trouve pas la cible
```bash
# Vérifier que l'application tourne
curl http://localhost:8080

# Vérifier le réseau Docker
docker network inspect ebc-network

# Lancer ZAP manuellement
docker run --rm --network ebc-network owasp/zap2docker-stable \
  zap-baseline.py -t http://nginx:80 -r report.html
```

### Trivy retourne trop de vulnérabilités
```bash
# Filtrer par sévérité
trivy image --severity CRITICAL,HIGH mon-image

# Ignorer les faux positifs
trivy image --ignorefile .trivyignore mon-image
```

### Gitleaks faux positifs
```toml
# Ajouter dans .gitleaks.toml
[[allowlist]]
paths = [
    "vendor/",
    "tests/",
    "*.md",
]
regexes = [
    "example",
    "test",
    "placeholder"
]
```

## 4. Problèmes Réseau

### Les conteneurs ne se voient pas entre eux
```bash
# Vérifier le réseau
docker network ls
docker network inspect ebc-network

# Connecter un conteneur au réseau
docker network connect ebc-network <container_name>
```

### Impossible d'accéder aux services depuis le navigateur
```bash
# Vérifier que les ports sont bien exposés
docker ps

# Vérifier le pare-feu
sudo ufw status
sudo ufw allow 8080/tcp
sudo ufw allow 9000/tcp
sudo ufw allow 3000/tcp
```

## 5. Réinitialisation Complète

```bash
# Arrêter et supprimer tous les conteneurs et volumes
docker-compose down -v

# Nettoyer les images non utilisées
docker system prune -a

# Réinstaller
./setup.sh
```

## 6. Erreurs Courantes et Solutions Rapides

| Erreur | Solution |
|--------|----------|
| `port is already allocated` | Changer le port dans docker-compose.yml |
| `Cannot find network` | `docker network create ebc-network` |
| `sonarqube: no space left` | `docker system prune` |
| `PHPStan not found` | `cd app/symfony && composer install` |
| `pytest: command not found` | `pip install -r ci-cd/scripts/api-tests/requirements.txt` |
| `git: command not found` | `sudo apt-get install git` |

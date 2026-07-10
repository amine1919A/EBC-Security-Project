# Guide de Dépannage

## Problèmes fréquents

### 1. Port 9000 déjà utilisé (SonarQube vs app)

**Symptôme :** `Error starting userland proxy: listen tcp4 0.0.0.0:9000: bind: address already in use`

**Solution :** L'application et SonarQube utilisaient tous les deux le port 9000. Correction déjà appliquée :
- SonarQube → `host:9000` (inchangé)
- App PHP-FPM → `host:9001 → internal:9000`

Si le problème persiste, tue le processus occupant le port :
```bash
sudo lsof -i :9000
kill -9 <PID>
```

### 2. Elasticsearch ne démarre pas

**Symptôme :** `ebc-elasticsearch` reste en `unhealthy` ou redémarre en boucle

**Solutions :**
- Augmenter `vm.max_map_count` sur l'hôte :
  ```bash
  sudo sysctl -w vm.max_map_count=262144
  ```
- Vérifier la RAM disponible (Elasticsearch nécessite 512 Mo minimum)
- Attendre 2 minutes (healthcheck a `start_period: 60s`)

### 3. App en 502 Bad Gateway

**Symptôme :** http://localhost:8080 renvoie 502

**Causes + solutions :**
- PHP-FPM pas prêt : attendre 10-15s après `docker compose up -d`
- Volume Symfony manquant : vérifier que `app/symfony/` n'est pas vide
- Rebuild complet :
  ```bash
  docker compose build --no-cache app
  docker compose up -d
  ```

### 4. Pipeline GitHub Actions rouge

**Symptôme :** Le workflow échoue sur GitHub

**Vérifications :**
- Les secrets `SONAR_TOKEN` et `SNYK_TOKEN` sont-ils configurés ? (Settings → Secrets)
- Le Dockerfile build-t-il en local ? `docker build -t test -f app/Dockerfile app/`
- Les jobs ont `continue-on-error: true` → l'échec d'un job ne bloque pas les autres
- Voir les logs sur https://github.com/amine1919A/EBC-Security-Project/actions

### 5. `composer install` échoue

**Symptôme :** Erreur lors de l'installation des dépendances PHP

**Solutions :**
- Vérifier que `composer.lock` existe : `ls app/symfony/composer.lock`
- Vider le cache Composer : `docker run --rm -v $(pwd)/app/symfony:/app composer clear-cache`
- Réessayer : `docker compose run --rm app composer install`

### 6. Grafana ne charge pas les dashboards

**Symptôme :** Dashboard "EBC Security KPIs" absent dans Grafana

**Solutions :**
- Redémarrer Grafana : `docker compose stop grafana && docker compose rm grafana && docker compose up -d grafana`
- Attendre 10s (provisioning asynchrone)
- Vérifier que le fichier dashboard est dans le bon dossier :
  ```bash
  docker exec ebc-grafana ls /var/lib/grafana/dashboards/
  ```

### 7. OWASP ZAP échoue dans le CI

**Symptôme :** Job DAST - OWASP ZAP échoue avec exit code 1

**Causes :**
- L'application n'est pas accessible sur `localhost:8080` au moment du scan
- Les conteneurs MySQL/Elasticsearch pas encore prêts
- Priorité : l'image docker est construite dans le même job `integration`, donc disponible

### 8. Token GitHub exposé

**Symptôme :** `remote: Invalid username or token. Password authentication is not supported for Git operations.`

**Solution :** Le token a été révoqué (bonne pratique). En créer un nouveau :
1. https://github.com/settings/tokens → Generate new token
2. Scope : `repo`
3. L'utiliser pour le push : `git push https://<user>:<token>@github.com/...`

### 9. MySQL unhealthy

**Symptôme :** `ebc-mysql` reste en unhealthy

**Solutions :**
- Vérifier les logs : `docker logs ebc-mysql --tail 20`
- Attendre 30s (premier démarrage plus lent)
- Réinitialiser le volume : `docker compose down -v && docker compose up -d`

## Commandes utiles

```bash
# Logs d'un service
docker logs ebc-app --tail 50
docker logs ebc-nginx --tail 50

# Shell dans un conteneur
docker exec -it ebc-app bash

# Rebuild complet
docker compose build --no-cache
docker compose up -d

# Réinitialisation complète
docker compose down -v
docker compose up -d

# État des healthchecks
docker inspect --format='{{json .State.Health.Status}}' ebc-mysql
```

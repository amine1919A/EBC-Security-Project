# Guide d'Utilisation - EBC Security Testing Platform

## Menu Principal

| Action | Commande |
|--------|----------|
| Démarrer tous les services | `./start.sh` |
| Arrêter tous les services | `./stop.sh` |
| Réinitialiser (supprimer données) | `./reset.sh` |
| Voir les logs | `docker-compose logs -f` |
| État des services | `docker ps` |

## Pipeline de Sécurité

### Exécution Manuelle

```bash
# SAST - Analyse statique
bash ci-cd/scripts/run-sast.sh

# DAST - Tests dynamiques
bash ci-cd/scripts/run-dast.sh http://localhost:8080

# SCA - Analyse dépendances
bash ci-cd/scripts/run-sca.sh

# Tests API
cd ci-cd/scripts/api-tests
pip install -r requirements.txt
pytest test_api.py -v --html=report.html
```

### Exécution Automatisée (CI/CD)

Le pipeline s'exécute automatiquement sur GitLab à chaque push sur `main` :

1. `security:sast_sonarqube` → Analyse SonarQube
2. `security:sast_phpstan` → Analyse PHPStan
3. `security:sca_trivy` → Scan Trivy
4. `security:secrets_gitleaks` → Détection secrets
5. `test:unit` → Tests unitaires
6. `test:api` → Tests API sécurité
7. `security:dast_zap` → Scan ZAP
8. `security:dast_nikto` → Scan Nikto
9. `build` → Construction image Docker
10. `deploy:staging` → Déploiement
11. `security:kpi_aggregate` → Métriques KPIs

## Accès aux Interfaces

| Service | URL | Login |
|---------|-----|-------|
| Application EBC | http://localhost:8080 | - |
| SonarQube | http://localhost:9000 | admin/admin |
| Grafana | http://localhost:3000 | admin/admin |
| Prometheus | http://localhost:9090 | - |

## Interprétation des Résultats

### SonarQube
- **Quality Gate PASSED** → Code de qualité acceptable
- **Bugs, Vulnerabilities, Code Smells** → Indique les problèmes
- **Security Hotspots** → Zones nécessitant revue manuelle

### OWASP ZAP
- **HIGH (Rouge)** → Vulnérabilité critique, action immédiate
- **MEDIUM (Orange)** → Vulnérabilité modérée, à corriger
- **LOW (Jaune)** → Information, à surveiller
- **INFORMATIONAL (Bleu)** → Note d'information

### Trivy
- **CRITICAL** → CVE avec score CVSS 9.0-10.0
- **HIGH** → CVE avec score CVSS 7.0-8.9
- **MEDIUM/LOW** → CVE avec score moindre

### Gitleaks
- **Secret found** → Mot de passe/token dans le code, rotation immédiate

## Gestion des Faux Positifs

Ajouter dans les fichiers de configuration :

```yaml
# SonarQube - sonar-project.properties
sonar.exclusions=vendor/**,tests/**,var/**

# Gitleaks - .gitleaks.toml (dans allowlist)
[[allowlist]]
paths = ["tests/", "docs/"]

# ZAP - dans la politique
<scanner>
    <id>40012</id>  <!-- ID du scanner -->
    <threshold>HIGH</threshold>  <!-- Ignorer si LOW -->
</scanner>
```

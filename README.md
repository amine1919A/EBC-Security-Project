# EBC Security Testing Platform

Plateforme **DevSecOps** automatisée pour l'application EBC (Symfony 6.4 / PHP 8.2).  
Intègre les outils SAST, DAST, SCA, Secrets & Monitoring dans un pipeline CI/CD complet.  
**Couverture OWASP Top 10 (2021) : 100%** ✅

## Démarrage Rapide

```bash
git clone https://github.com/amine1919A/EBC-Security-Project.git
cd EBC-Security-Project
chmod +x setup.sh && ./setup.sh
```

## Services Disponibles

| Service | URL | Identifiants |
|---------|-----|-------------|
| Application EBC | http://localhost:8080 | - |
| SonarQube (SAST) | http://localhost:9000 | admin / admin |
| Grafana (Monitoring) | http://localhost:3000 | admin / admin |
| Prometheus (Métriques) | http://localhost:9090 | - |

## Documentation

| Document | Description |
|----------|-------------|
| [Installation](docs/01-installation.md) | Prérequis, setup, vérification |
| [Utilisation](docs/02-utilisation.md) | Tests, pipeline, dashboard Grafana |
| [Architecture](docs/03-architecture.md) | Diagrammes, flux CI, mapping OWASP |
| [Dépannage](docs/04-troubleshooting.md) | Problèmes fréquents et solutions |
| [Rapport de validation](docs/05-rapport-validation.md) | Résultats pipeline, métriques |

## Pipeline CI/CD (11 jobs)

```
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  ┌─────────┐  ┌──────┐
│  Build  │  │   SAST   │  │   SCA    │  │ Secrets│  │  Tests  │  │ KPIs │
│  Docker │→│Sonar/Stan│→│Trivy/Snyk│→│Gitleaks│→│ PHP/API │→│Grafana│
└─────────┘  └──────────┘  └──────────┘  └────────┘  └────┬────┘  └──────┘
                                                          │
                                                    ┌─────▼─────┐
                                                    │   DAST    │
                                                    │ ZAP/Nikto │
                                                    └───────────┘
```

## OWASP Top 10 — Couverture

| # | Catégorie | Outils | Statut |
|---|-----------|--------|--------|
| A01 | Broken Access Control | Tests API + PHPStan + ZAP | ✅ |
| A02 | Cryptographic Failures | Tests API + SonarQube + Trivy | ✅ |
| A03 | Injection (SQL, XSS, XXE, CMD) | Tests API + SonarQube + ZAP | ✅ |
| A04 | Insecure Design | Tests API (rate limit, lockout) | ✅ |
| A05 | Security Misconfiguration | Tests API + Nikto + SonarQube | ✅ |
| A06 | Vulnerable Components | Trivy + Snyk + ZAP | ✅ |
| A07 | Authentication Failures | Tests API + PHPStan | ✅ |
| A08 | Data Integrity Failures | Tests API (CSRF, deserialization) | ✅ |
| A09 | Logging & Monitoring | Tests API + Prometheus + Grafana | ✅ |
| A10 | SSRF | Tests API | ✅ |

## KPIs

- **Temps de détection** : < 12 minutes (vs semaines sans automatisation)
- **Couverture OWASP** : 100% (10/10 catégories)
- **Faux positifs** : < 5%
- **Impact pipeline** : ~12 min additionnels
- **Portabilité** : `git clone + setup.sh` sur tout Linux avec Docker

## Réinitialisation du token GitHub

Le token initial a été révoqué (sécurité). Pour pusher :

1. Créer un token : https://github.com/settings/tokens (scope: `repo`)
2. Utiliser : `git push https://<user>:<token>@github.com/amine1919A/EBC-Security-Project.git main`

## Auteur

**amine1919A** — amine.abdelli1919@gmail.com  
Projet académique — Université

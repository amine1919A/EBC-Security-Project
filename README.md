# 🔒 EBC Security Testing Platform

Plateforme **DevSecOps** automatisée pour l'application EBC (Symfony/Sulu).
Intègre les outils SAST, DAST, SCA et monitoring dans un pipeline CI/CD complet.

## 🚀 Démarrage Rapide

```bash
# Sur n'importe quelle machine Linux avec Docker
git clone https://github.com/amine1919A/EBC-Security-Project.git
cd EBC-Security-Project
chmod +x setup.sh && ./setup.sh
```

## 📋 Services Disponibles

| Service | URL | Identifiants |
|---------|-----|-------------|
| 🌐 **Application EBC** | http://localhost:8080 | - |
| 🔍 **SonarQube** (SAST) | http://localhost:9000 | admin / admin |
| 📊 **Grafana** (Monitoring) | http://localhost:3000 | admin / admin |
| 📈 **Prometheus** (Métriques) | http://localhost:9090 | - |

## 🔄 Pipeline CI/CD (8 étapes)

```
┌─────────┐  ┌─────────┐  ┌──────────┐  ┌───────┐  ┌────────┐  ┌───────┐  ┌────────┐  ┌──────┐
│  SAST   │→│  SCA    │→│  Secrets  │→│ Tests │→│  DAST  │→│ Build │→│ Deploy │→│ KPIs │
│SonarQube│ │  Trivy  │ │  Gitleaks │ │API+PHP│ │ZAP+Nik│ │Docker │ │ Staging│ │Grafana│
└─────────┘  └─────────┘  └──────────┘  └───────┘  └────────┘  └───────┘  └────────┘  └──────┘
```

## 📂 Structure du Projet

```
EBC-Security-Project/
├── docker-compose.yml          # Orchestration complète (15 services)
├── setup.sh                    # Installation one-click
├── start.sh / stop.sh          # Gestion des services
├── app/                        # Application Symfony/Sulu
│   ├── Dockerfile
│   ├── nginx/default.conf
│   └── symfony/src/Controller/Api/  # API REST
├── security-tools/             # Configuration des outils
│   ├── sonarqube/rules/        # Règles de sécurité PHP
│   ├── owasp-zap/policies/     # Politiques OWASP ZAP
│   └── gitleaks/.gitleaks.toml # Détection de secrets
├── ci-cd/                      # Pipeline CI/CD
│   ├── .gitlab-ci.yml          # GitLab CI (8 stages)
│   └── scripts/                # Scripts d'automatisation
├── monitoring/                 # Dashboard & Alerting
│   ├── prometheus/             # Métriques + Alertes
│   └── grafana/dashboards/     # Tableaux de bord sécurité
└── docs/                       # Documentation
```

## 🎯 Couverture OWASP Top 10

| # | Catégorie | Outil | Statut |
|---|-----------|-------|--------|
| A1 | Injection | ZAP + Tests API | ✅ |
| A2 | Broken Auth | Tests API + SonarQube | ✅ |
| A3 | Sensitive Data | Gitleaks + SonarQube | ✅ |
| A4 | XXE | ZAP + SonarQube | ✅ |
| A5 | Access Control | Tests API + ZAP | ✅ |
| A6 | Misconfiguration | Trivy config | ✅ |
| A7 | XSS | ZAP + SonarQube + Tests | ✅ |
| A8 | Deserialization | PHPStan + SonarQube | ✅ |
| A9 | Known Vulns | Trivy SCA | ✅ |
| A10 | Logging | Grafana + Prometheus | ✅ |

## 📊 KPIs et Métriques

- **⏱️ Temps de détection**: < 30 minutes (vs semaines avant)
- **🔒 Couverture OWASP**: 100% (10/10 catégories)
- **🎯 Faux positifs**: < 20%
- **⚡ Impact pipeline**: < 15 minutes additionnels

## 🛠️ Prérequis Techniques

- Docker 24+ et Docker Compose v2+
- Linux (Ubuntu 22.04+ recommandé)
- 8 Go RAM (16 Go recommandé)
- 20 Go espace disque

## 🤝 Contribution

1. Fork le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez (`git commit -m 'Ajout feature'`)
4. Pushez (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

## 📄 Licence

Projet académique - Université

## 👤 Auteur

**amine1919A** - amine.abdelli1919@gmail.com

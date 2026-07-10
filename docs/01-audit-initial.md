# Rapport d'Audit Initial de Sécurité

**Projet** : EBC Security Testing Platform  
**Date** : Juillet 2026  
**Version** : 1.0  
**Classification** : Confidentiel  

---

## 1. Périmètre de l'Audit

### 1.1 Application Cible
- **Nom** : EBC (Enterprise Business Collaboration)
- **Framework** : Symfony 6.4 avec Sulu CMS
- **API** : REST via API Platform
- **Base de données** : MySQL 8.0
- **Moteur de recherche** : Elasticsearch 7.17
- **Conteneurisation** : Docker + Docker Compose

### 1.2 Architecture Technique
```
[Utilisateur] → [Nginx] → [PHP-FPM 8.2] → [Symfony 6.4]
                              ├── [MySQL 8.0]
                              └── [Elasticsearch 7.17]
```

---

## 2. Cartographie des Flux de Données

### 2.1 Points d'Entrée (Attack Surface)

| Point d'entrée | Méthode | Authentification | Données sensibles |
|---------------|---------|-----------------|-------------------|
| `/api/health` | GET | Non | Aucune |
| `/api/auth/login` | POST | Non | Identifiants |
| `/api/users` | GET | Oui (JWT) | Données utilisateurs |
| `/api/admin/*` | GET/POST | Oui (Admin) | Données critiques |
| `/api/search` | GET | Non | Requêtes utilisateur |
| `/api/feedback` | POST | Non | Messages utilisateur |
| `/api/security/*` | GET/POST | Oui | Rapports sécurité |

### 2.2 Flux de Données Sensibles

```
Client → POST /api/auth/login → [Identifiants en JSON]
Client → GET /api/users/{id}  → [Token JWT en Header]
App    → MySQL               → [MDP en clair .env]
App    → Elasticsearch       → [Données indexées]
```

### 2.3 Exposition Actuelle

| Faiblesse identifiée | Niveau risque | Impact |
|---------------------|---------------|--------|
| Mots de passe dans `.env` | 🔴 CRITIQUE | Exposition credentials |
| Pas de JWT implémenté | 🔴 CRITIQUE | Pas d'authentification |
| Pas de rate limiting | 🟠 ÉLEVÉ | Brute-force possible |
| SQL Injection non testée | 🟠 ÉLEVÉ | Fuite de données |
| XSS non filtré | 🟠 ÉLEVÉ | Vol de session |
| Headers sécurité manquants | 🟡 MOYEN | Clickjacking/XSS |
| Version PHP visible | 🟡 MOYEN | Fingerprinting |
| Stack trace verbose | 🟢 FAIBLE | Information leak |

---

## 3. Analyse des Dépendances Critiques

### 3.1 Stack Technique

| Composant | Version | Risque | Alternative |
|-----------|---------|--------|-------------|
| PHP | 8.2 | 🟢 Faible | - |
| Symfony | 6.4 | 🟢 Faible | - |
| MySQL | 8.0 | 🟢 Faible | MariaDB |
| Elasticsearch | 7.17 | 🟡 Moyen | Opensearch |
| Nginx | latest | 🟢 Faible | Apache |

### 3.2 Dépendances PHP (via composer.json)

| Package | Risque sécurité | Notes |
|---------|----------------|-------|
| symfony/framework-bundle | 🟢 Faible | Maintenu activement |
| doctrine/orm | 🟢 Faible | Sécurisé par défaut |
| api-platform/core | 🟡 Moyen | Surveiller CVE |
| phpstan/phpstan | 🟢 Faible | Outil d'analyse |

---

## 4. Configuration de Sécurité Existante

### 4.1 Ce qui est en place
- ✅ Conteneurisation Docker (isolation)
- ✅ PHP 8.2 (version supportée)
- ✅ Framework Symfony (sécurisé par défaut)
- ✅ API Platform (validation entrées)

### 4.2 Ce qui manque
- ❌ Analyse statique (SonarQube/PHPStan)
- ❌ Tests dynamiques (OWASP ZAP)
- ❌ Analyse dépendances (Trivy)
- ❌ Détection secrets (Gitleaks)
- ❌ Tests API automatisés
- ❌ Monitoring sécurité (Grafana)
- ❌ Pipeline CI/CD automatisé
- ❌ Headers de sécurité HTTP
- ❌ Rate limiting
- ❌ Authentification JWT

---

## 5. Score de Maturité Sécurité (Initial)

| Catégorie | Score actuel | Score cible |
|-----------|-------------|-------------|
| SAST (Analyse statique) | 0/10 | 8/10 |
| DAST (Tests dynamiques) | 0/10 | 8/10 |
| SCA (Dépendances) | 2/10 | 8/10 |
| Secrets Detection | 0/10 | 9/10 |
| Tests sécurité API | 0/10 | 8/10 |
| Monitoring | 1/10 | 8/10 |
| CI/CD Intégré | 0/10 | 9/10 |

**Score global initial** : **3/10** ⚠️  
**Score global cible** : **8.5/10** 🎯  

---

## 6. Recommandations Prioritaires

### Priorité 1 — Critique (Immédiat)
1. Mettre en place l'authentification JWT
2. Ajouter les headers de sécurité HTTP
3. Implémenter le rate limiting
4. Masquer les versions des serveurs

### Priorité 2 — Élevé (Sous 30 jours)
5. Déployer SonarQube pour l'analyse statique
6. Configurer OWASP ZAP pour les scans dynamiques
7. Intégrer Trivy pour l'analyse des dépendances
8. Ajouter Gitleaks pour la détection de secrets

### Priorité 3 — Moyen (Sous 60 jours)
9. Développer les tests API automatisés
10. Configurer Grafana + Prometheus
11. Implémenter le pipeline CI/CD complet
12. Former les équipes

---

## 7. Métriques de Base

| Métrique | Valeur initiale | Source |
|----------|----------------|--------|
| Nombre d'endpoints | 12 | Code review |
| Endpoints sans auth | 5 | Code review |
| Dépendances critiques | 45 | composer.json |
| CVE connues (estimation) | 3-5 | Base OWASP |
| Temps détection vulnérabilité | ~4 semaines | Manuel |
| Couverture tests sécurité | 0% | Aucun test |

---

**Rapport généré par :** Équipe Sécurité EBC  
**Prochaine révision :** Semaine 13 (post-déploiement)

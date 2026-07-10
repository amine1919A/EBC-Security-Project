# Matrice Comparative des Outils de Sécurité

**Objectif** : Sélectionner les outils les plus adaptés pour la plateforme EBC  
**Date** : Juillet 2026  
**Critères** : Efficacité, intégration Docker, coût, communauté, maintenance

---

## 1. SAST — Analyse Statique du Code

### Comparatif : SonarQube vs Alternatives

| Critère | SonarQube Community | PHPStan | Psalm | Phan |
|---------|-------------------|---------|-------|------|
| **Type** | Plateforme SAST | Analyseur PHP | Analyseur PHP | Analyseur PHP |
| **Langages** | 30+ | PHP uniquement | PHP uniquement | PHP uniquement |
| **Règles sécurité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Faux positifs** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Qualité code** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Docker officiel** | ✅ | ✅ (via PHP) | ✅ (via PHP) | ✅ (via PHP) |
| **Intégration GitLab** | ✅ Excellente | ✅ Bonne | ✅ Bonne | ✅ Bonne |
| **Documentation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Communauté** | Très grande | Grande | Moyenne | Petite |
| **Licence** | Community (gratuit) | MIT | MIT | MIT |
| **Courbe apprentissage** | Moyenne | Faible | Faible | Moyenne |

### Sélection Finale : **SonarQube Community + PHPStan**
- **SonarQube** : Plateforme centralisée, historique des analyses, Quality Gate, multi-langages
- **PHPStan** : Complément pour l'analyse PHP avancée (niveau max)

---

## 2. DAST — Tests Dynamiques

### Comparatif : OWASP ZAP vs Alternatives

| Critère | OWASP ZAP | Burp Suite | Nikto | Wapiti |
|---------|-----------|------------|-------|--------|
| **Type** | Proxy/Scanner | Proxy/Scanner | Scanner | Scanner |
| **Automatisation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **CI/CD Ready** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Docker officiel** | ✅ | ❌ (Pro only) | ✅ | ✅ |
| **OWASP Top 10** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **API Scan** | ✅ | ✅ | ❌ | ✅ |
| **Rapports HTML** | ✅ | ✅ | ✅ | ✅ |
| **Coût** | Gratuit | Gratuit (Communauté) | Gratuit | Gratuit |
| **Documentation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Communauté** | Très grande | Grande | Moyenne | Petite |

### Sélection Finale : **OWASP ZAP + Nikto**
- **ZAP** : Baseline, API Scan, Full Scan — couverture complète
- **Nikto** : Scan complémentaire rapide pour les serveurs web

---

## 3. SCA — Analyse des Dépendances

### Comparatif : Trivy vs Snyk

| Critère | Trivy | Snyk | Grype | Dependency-Check |
|---------|-------|------|-------|-----------------|
| **Type** | Scanner conteneur | Plateforme SCA | Scanner | Plugin |
| **Conteneurs** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Systèmes fichiers** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Base CVE** | NVD, RedHat, Debian | NVD + propre | NVD, RedHat | NVD |
| **Vitesse** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Docker officiel** | ✅ | ✅ | ✅ | ✅ |
| **CI/CD GitLab** | ✅ Excellente | ✅ Bonne | ✅ Bonne | ✅ Bonne |
| **Coût** | Gratuit | Gratuit (200 tests/mois) | Gratuit | Gratuit |
| **SBOM** | ✅ (CycloneDX) | ✅ | ✅ (CycloneDX) | ❌ |
| **Licence** | Apache 2.0 | Propriétaire | Apache 2.0 | Apache 2.0 |

### Sélection Finale : **Trivy + Snyk**
- **Trivy** : Rapide, complet, open-source, support conteneurs + filesystem + config
- **Snyk** : Complément pour les dépendances applicatives (PHP Composer)

---

## 4. IAST — Tests Interactifs Runtime

### Comparatif : Contrast Security vs Alternatives

| Critère | Contrast Security | Hdiv | Acunetix |
|---------|------------------|------|----------|
| **Type** | IAST (Agent) | IAST (Agent) | DAST/IAST |
| **Détection runtime** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Faux positifs** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Docker compatible** | ✅ | ✅ | ✅ |
| **CI/CD Intégration** | ✅ | ✅ | ✅ |
| **Prix** | Trial gratuit (14j) | Payant | Payant |
| **Documentation** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

### Sélection Finale : **Contrast Security (Trial)**
- Trial de 14 jours pour la phase de test
- Alternative open-source envisagée : **OWASP Glue** (en attente)

---

## 5. Détection de Secrets

### Comparatif : Gitleaks vs Alternatives

| Critère | Gitleaks | TruffleHog | GitGuardian | Talisman |
|---------|----------|------------|-------------|----------|
| **Patterns** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Vitesse** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Docker officiel** | ✅ | ✅ | ❌ | ❌ |
| **CI/CD GitLab** | ✅ Excellente | ✅ Bonne | ✅ | ✅ |
| **Faux positifs** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Configuration** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Coût** | Gratuit | Gratuit | Gratuit (limité) | Gratuit |

### Sélection Finale : **Gitleaks**
- Rapide, configurable, excellent support CI/CD
- Patterns personnalisables pour EBC

---

## 6. Monitoring et Dashboard

### Comparatif : Grafana vs Alternatives

| Critère | Grafana + Prometheus | Kibana + Elastic | Datadog |
|---------|---------------------|------------------|---------|
| **Type** | Dashboard + Métriques | Dashboard + Logs | SaaS Monitoring |
| **Sources de données** | 30+ | Elasticsearch only | Propriétaire |
| **Alerting** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Docker** | ✅ | ✅ | Agent only |
| **Coût** | Gratuit | Gratuit | Payant |
| **Personnalisation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

### Sélection Finale : **Grafana + Prometheus**
- Solution open-source complète, auto-hébergée
- Intégration facile avec tous les outils

---

## 7. Récapitulatif des Outils Sélectionnés

| Catégorie | Outil Principal | Outil Secondaire | Coût Total |
|-----------|----------------|-----------------|------------|
| SAST | SonarQube Community | PHPStan | 0€ |
| DAST | OWASP ZAP | Nikto | 0€ |
| SCA | Trivy | Snyk | 0€ (Snyk: 200 tests/mois gratuits) |
| IAST | Contrast Security (Trial) | - | 0€ (14 jours trial) |
| Secrets | Gitleaks | - | 0€ |
| Monitoring | Grafana + Prometheus | - | 0€ |
| CI/CD | GitLab CI / GitHub Actions | - | 0€ |
| **TOTAL** | | | **0€** ✅ |

---

## 8. Décisions Architecturales

| Décision | Justification |
|----------|---------------|
| Tout en Docker | Portabilité, isolation, reproduction facile |
| GitLab CI + GitHub Actions | Compatible GitHub, pipeline complet |
| Conteneurs séparés par outil | Indépendance, scalabilité |
| Grafana provisioning automatique | Dashboards pré-configurés, zéro configuration |
| Scripts shell d'automatisation | Fonctionne sans CI/CD, test local possible |

---

**Matrice validée par :** Équipe Sécurité EBC  
**Version** : 1.0  
**Prochaine revue** : Semaine 12 (post-implémentation)

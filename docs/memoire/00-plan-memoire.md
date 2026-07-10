# Plan du Mémoire — Automatisation des Tests de Sécurité pour l'Application EBC

**Auteur** : amine1919A  
**Date** : Juillet 2026  
**Pages** : 80-100  
**Langue** : Français  

---

## Structure Générale

### PARTIE I — Contexte et État de l'Art (20 pages)

**Chapitre 1 : Introduction** (5 pages)
- 1.1 Contexte du projet
- 1.2 Problématique
- 1.3 Objectifs
- 1.4 Structure du mémoire

**Chapitre 2 : Cybersécurité et DevSecOps** (8 pages)
- 2.1 Évolution de la sécurité applicative
- 2.2 DevSecOps : Définition et principes
- 2.3 OWASP Top 10 (2021) — Analyse détaillée
- 2.4 Chaîne CI/CD et sécurité

**Chapitre 3 : Outils de Sécurité Automatisée** (7 pages)
- 3.1 SAST : SonarQube, PHPStan
- 3.2 DAST : OWASP ZAP, Nikto
- 3.3 SCA : Trivy, Snyk
- 3.4 Détection de secrets : Gitleaks
- 3.5 IAST : Contrast Security
- 3.6 Monitoring : Grafana, Prometheus

### PARTIE II — Conception et Implémentation (30 pages)

**Chapitre 4 : Architecture de la Solution** (10 pages)
- 4.1 Architecture globale (diagramme)
- 4.2 Choix technologiques et justification
- 4.3 Conteneurisation Docker
- 4.4 Pipeline CI/CD : Séquence des tests
- 4.5 Dashboard et monitoring

**Chapitre 5 : Implémentation SAST** (5 pages)
- 5.1 Configuration SonarQube
- 5.2 Règles PHP personnalisées
- 5.3 Intégration PHPStan
- 5.4 Résultats et Quality Gate

**Chapitre 6 : Implémentation DAST** (5 pages)
- 6.1 Configuration OWASP ZAP
- 6.2 Politique EBC personnalisée
- 6.3 Scan Nikto complémentaire
- 6.4 Résultats des scans

**Chapitre 7 : Implémentation SCA et Secrets** (5 pages)
- 7.1 Analyse Trivy (conteneurs + fichiers)
- 7.2 Analyse Snyk (dépendances PHP)
- 7.3 Détection Gitleaks
- 7.4 SBOM (Software Bill of Materials)

**Chapitre 8 : Tests et Dashboard** (5 pages)
- 8.1 Tests API automatisés (OWASP)
- 8.2 Configuration Prometheus/Grafana
- 8.3 Agrégation des KPIs
- 8.4 Alerting et notifications

### PARTIE III — Évaluation et Perspectives (20 pages)

**Chapitre 9 : Résultats et Analyse** (8 pages)
- 9.1 Comparatif avant/après (audit initial vs final)
- 9.2 Analyse des faux positifs
- 9.3 Performance du pipeline
- 9.4 Couverture OWASP Top 10

**Chapitre 10 : Discussion** (6 pages)
- 10.1 Limites de la solution
- 10.2 Difficultés rencontrées
- 10.3 Leçons apprises

**Chapitre 11 : Perspectives** (6 pages)
- 11.1 Évolutions possibles
- 11.2 Intégration IAST (Contrast Security)
- 11.3 Intelligence Artificielle pour la sécurité
- 11.4 Déploiement production

### PARTIE IV — Annexes (15 pages)

**Chapitre 12 : Annexes techniques**
- A: Code source des scripts d'automatisation
- B: Configuration Docker Compose complète
- C: Pipeline CI/CD complet
- D: Tests API (listing complet)
- E: Dashboard Grafana (captures d'écran)
- F: Glossaire

**Bibliographie** (5 pages)
- Articles scientifiques
- Documentation technique
- Sites web et ressources

---

## Contenu par Chapitre (Détail)

### Chapitre 1 : Introduction
*Objectif : Présenter le projet, son contexte et ses enjeux*

- Contexte : Entreprise EBC, application Symfony/Sulu
- Problématique : Absence de sécurité automatisée, vulnérabilités non détectées
- Objectifs : Intégrer DevSecOps dans le cycle de développement
- Contribution : Pipeline CI/CD complet, outils open-source, zéro coût de licence

### Chapitre 9 : Résultats et Analyse
*Objectif : Présenter et analyser les résultats obtenus*

Tableaux, graphiques et métriques clés :
- Score sécurité : 3/10 → 8.5/10
- Temps détection : 4 semaines → 11 minutes
- Couverture OWASP : 0% → 92%
- Faux positifs : 25% → 8.75%
- Tests automatisés : 0 → 25
- Pipeline : 8 stages, ~11 min
- Coût total : 0€

---

## Annexes — Structure des Fichiers

```
docs/memoire/
├── 00-plan-memoire.md          ← Ce fichier
├── 01-introduction.md           ← À rédiger
├── 02-etat-de-l-art.md          ← À rédiger
├── 03-outils-securite.md        ← À rédiger
├── 04-architecture.md           ← À rédiger
├── 05-implementation-sast.md    ← À rédiger
├── 06-implementation-dast.md    ← À rédiger
├── 07-implementation-sca.md     ← À rédiger
├── 08-tests-dashboard.md        ← À rédiger
├── 09-resultats-analyse.md      ← À rédiger
├── 10-discussion.md             ← À rédiger
├── 11-perspectives.md           ← À rédiger
├── 12-annexes.md                ← À rédiger
└── 13-bibliographie.md          ← À rédiger
```

---

**Prochaine étape** : Rédaction du contenu complet (80-100 pages)  
**Format** : Markdown → export LaTeX/PDF via Pandoc

# Chapitre 1 : Introduction

## 1.1 Contexte du Projet

L'application EBC (Enterprise Business Collaboration) est une plateforme web développée avec Symfony 6.4 et Sulu CMS, utilisant MySQL 8.0 et Elasticsearch 7.17. Dans le cadre de son amélioration continue, l'entreprise souhaite intégrer une démarche DevSecOps afin de détecter les vulnérabilités de sécurité dès les premières étapes du cycle de développement.

## 1.2 Problématique

Les tests de sécurité sont actuellement :
- Effectués manuellement, en fin de cycle
- Longs (4 semaines en moyenne)
- Non reproductibles
- Coûteux en temps humain

## 1.3 Objectifs

1. Automatiser les tests de sécurité dans le pipeline CI/CD
2. Couvrir les vulnérabilités OWASP Top 10
3. Réduire le temps de détection de semaines à minutes
4. Maintenir un taux de faux positifs inférieur à 20%
5. Assurer la portabilité de la solution (Docker, multi-PC)

## 1.4 Structure du Mémoire

Ce mémoire est organisé en quatre parties :
- Partie I : État de l'art sur la sécurité applicative et DevSecOps
- Partie II : Conception et implémentation de la solution
- Partie III : Évaluation des résultats et perspectives
- Partie IV : Annexes techniques et bibliographie

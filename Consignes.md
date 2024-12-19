### Projet MLOps - Déploiement automatisé d'une solution ML
Échéance :20 décembre 2024 23:59

## Objectif
Mettre en place une chaîne complète MLOps en intégrant l'ensemble des pratiques DevOps et les outils spécifiques au Machine Learning, en utilisant une approche d'Infrastructure as Code (IaC) et de CI/CD.

## Organisation
- Projet en groupe de 3 étudiants
- Date de rendu : 20 décembre 2024
- Livrable : Repository GitHub contenant l'ensemble du code et de la documentation

## Technologies requises
- Conteneurisation : Docker
- IaC : Terraform (ou équivalent : OpenTofu, Pulumi)
- Configuration : Ansible (ou équivalent : Terraform)
- Cloud : AWS (ou Azure/GCP/OVH/ScaleWay/...)
- ML Tracking : MLflow
- CI/CD : GitHub Actions (ou équivalent : Gitlab CI, Jenkins, ...)
- Monitoring : Prometheus + Grafana

### Attendus du projet
## Infrastructure
- Mise en place de l'infrastructure cloud via Terraform
- Configuration des serveurs via Ansible
- Architecture containerisée avec Docker
- Documentation des choix d'architecture

## Application ML
Deux options possibles :

- Développement d'un modèle ML simple
- Utilisation d'une API ML existante
L'application doit inclure :

- Une API permettant de faire des prédictions
- Un système de versioning des modèles avec MLflow
- Un pipeline d'entraînement/déploiement automatisé

## Pipeline CI/CD
Mise en place avec GitHub Actions :

- Tests automatisés
- Build des images Docker
- Déploiement automatique

## Monitoring
- Métriques d'infrastructure avec Prometheus
- Visualisation avec Grafana

## Documentation
Le repository doit contenir :

- README détaillé avec architecture et choix techniques
- Guide d'installation pas à pas
- Documentation des APIs
- Guides de troubleshooting (falcultatif)
- Commentaires pertinents dans le code

## Critères d'évaluation
- Qualité du code et respect des bonnes pratiques
- Clarté et exhaustivité de la documentation
- Fonctionnalité du projet
- Automatisation des processus
- Pertinence des tests
- Qualité du monitoring

## Bonus
- Gestion des secrets (vault, AWS Secrets Manager, etc.)
- Tests de charge
- Interface utilisateur
- Haute disponibilité
- Gestion des backups
- Alerting
- Gestion des environnements (dev/prod)
- Monitoring des performances du modèle

## Conseils
- Privilégiez un projet simple mais fonctionnel
- Procédez par étapes et validez chaque composant
- Documentez au fur et à mesure
- Utilisez des branches Git pour le développement
- Ajoutez des technologies complémentaires pertinentes si cela vous semble nécessaire ou utile

## Important
- Vérifiez régulièrement les coûts cloud
- Nettoyez les ressources inutilisées
- Utilisez des instances de petite taille pour le développement
- Le code doit être accessible et exécutable en suivant uniquement la documentation fournie.
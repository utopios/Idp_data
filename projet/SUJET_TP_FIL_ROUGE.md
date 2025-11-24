# TP FIL ROUGE : PLATEFORME MLOPS POUR SCORING DE CRÉDIT

## CONTEXTE MÉTIER

**Entreprise** : "Prêt à dépenser" - Société financière
**Problématique** : Développer une plateforme MLOps industrielle pour déployer et gérer un système de scoring crédit
**Public cible** : Personnes avec peu ou pas d'historique de crédit
**Enjeu** : Construire une infrastructure complète, scalable et automatisée pour le cycle de vie ML avec un focus fort sur le Data Engineering

---

## OBJECTIFS PÉDAGOGIQUES

### Compétences Data Engineering (Focus 60%)

#### 1. Pipelines de données et ETL
- Conception de pipelines ETL robustes et scalables
- Ingestion de données multi-sources (8 fichiers CSV, 2.5GB)
- Data quality et validation automatisée
- Optimisation du stockage (Parquet, compression, partitionnement)
- Versioning des artefacts de données

#### 2. Infrastructure et Containerisation
- Dockerisation d'applications ML complètes
- Orchestration avec Docker Compose
- Infrastructure as Code
- Gestion des environnements (dev, staging, production)
- Optimisation des images (multi-stage builds)

#### 3. Déploiement et Scalabilité
- Déploiement sur Kubernetes
- Manifests K8s (Deployments, Services, Ingress, HPA)
- Helm charts pour packaging
- Auto-scaling et load balancing
- Gestion des secrets et configurations

#### 4. CI/CD et Automatisation
- Pipelines CI/CD complètes (GitHub Actions ou équivalent)
- Tests automatisés (unitaires, intégration, e2e)
- Déploiement continu multi-environnements
- GitOps et versioning
- Rollback strategies

#### 5. Orchestration de workflows
- Apache Airflow (ou Cloud Composer sur GCP)
- DAGs pour pipelines ML end-to-end
- Scheduling et dépendances complexes
- Monitoring et retry logic
- Custom operators si nécessaire

#### 6. Observabilité et Monitoring
- Prometheus + Grafana (ou Cloud Monitoring sur GCP)
- Logs centralisés
- Alerting intelligent et SLA
- Drift detection (données et modèle)
- Dashboards métier et techniques

### Compétences Machine Learning (Focus 40%)

#### 7. Développement et optimisation de modèles
- Comparaison de multiples algorithmes (5+ modèles)
- Feature engineering avancé
- Gestion du déséquilibre des classes
- Optimisation des hyperparamètres (Optuna, GridSearchCV)
- Validation croisée stratifiée

#### 8. Métriques métier et seuil de décision
- Définition de fonctions de coût métier (FN vs FP)
- Optimisation du seuil de classification
- Métriques business (coût d'erreur, ROI)
- Métriques techniques (AUC-ROC, Precision, Recall, F1)

#### 9. MLOps et déploiement de modèles
- MLflow pour tracking, registry et serving
- Versioning de modèles
- Promotion de modèles (Staging → Production)
- API de prédiction (FastAPI)
- Model serving scalable

#### 10. Interprétabilité et conformité
- Feature importance globale
- SHAP values pour explications locales
- Documentation des décisions modèle
- Transparence pour conformité RGPD

---

## STACK TECHNIQUE

### Outils obligatoires

**Infrastructure et DevOps** :
- Docker, Docker Compose
- Kubernetes, Helm
- GitHub Actions (ou GitLab CI)
- PostgreSQL

**Data Engineering** :
- Pandas, NumPy
- Parquet, compression
- Great Expectations ou Pydantic
- Apache Airflow

**Machine Learning** :
- MLflow (Tracking, Registry, Serving)
- Scikit-learn
- LightGBM, XGBoost
- Optuna ou GridSearchCV
- SHAP

**API et Serving** :
- FastAPI
- Uvicorn

**Monitoring** :
- Prometheus, Grafana
- Evidently AI (drift detection)

### Outils optionnels (Google Cloud Platform)

Les stagiaires peuvent choisir d'utiliser des services GCP en remplacement ou en complément :

- **Cloud Storage** : Stockage des données et artefacts
- **BigQuery** : Data warehouse pour analytics
- **Cloud Composer** : Remplacement d'Airflow (managé)
- **Google Kubernetes Engine (GKE)** : Cluster K8s managé
- **Cloud Build** : Remplacement de GitHub Actions
- **Cloud Monitoring** : Remplacement de Prometheus/Grafana
- **Artifact Registry** : Stockage d'images Docker
- **Secret Manager** : Gestion des secrets
- **Cloud Run** : Déploiement serverless (alternative à K8s)
- **Vertex AI** : Alternative à MLflow (pipelines ML managés)

**Note importante** : L'utilisation de GCP est optionnelle. Le TP peut être réalisé entièrement en local ou avec des outils open source. Si GCP est utilisé, attention aux coûts (utiliser le free tier et bien nettoyer les ressources).

---

## DONNÉES

### Source
**Kaggle** : Home Credit Default Risk
**Lien** : https://www.kaggle.com/c/home-credit-default-risk/data

### Volume total
- **~2.5 GB** (8 fichiers CSV)
- **307,511** lignes d'entraînement
- **48,744** lignes de test
- **~8%** de déséquilibre (clients en défaut minoritaires)

### Fichiers à télécharger
1. `application_train.csv` (166 MB) - Données principales d'entraînement
2. `application_test.csv` (27 MB) - Données de test
3. `bureau.csv` (170 MB) - Historique bureau de crédit
4. `bureau_balance.csv` (376 MB) - Balances mensuelles
5. `POS_CASH_balance.csv` (393 MB) - Historique POS/Cash
6. `credit_card_balance.csv` (425 MB) - Balances carte de crédit
7. `previous_application.csv` (405 MB) - Demandes de crédit précédentes
8. `installments_payments.csv` (723 MB) - Historique des paiements
9. `HomeCredit_columns_description.csv` - Description des colonnes

### Schéma relationnel
```
application_train (SK_ID_CURR) ← Table principale
    ├── bureau (SK_ID_CURR)
    │   └── bureau_balance (SK_ID_BUREAU)
    ├── previous_application (SK_ID_CURR)
    ├── POS_CASH_balance (SK_ID_CURR)
    ├── credit_card_balance (SK_ID_CURR)
    └── installments_payments (SK_ID_CURR)
```

---

## PLANNING DU TP

### PARTIE 1 : Pipeline ETL et Feature Engineering

**Objectifs** :
- Construire un pipeline ETL robuste et reproductible
- Implémenter des data quality checks automatiques
- Créer des features avancées à partir des 8 sources de données
- Optimiser le stockage pour de gros volumes
- Versioning des données transformées

**Livrables attendus** :

1. **Module d'ingestion des données**
   - Chargement des 8 fichiers CSV
   - Validation des schémas (types, contraintes, clés primaires)
   - Détection des anomalies (outliers, valeurs nulles excessives, duplicats)
   - Logs structurés pour traçabilité
   - Rapport de qualité automatique (HTML ou PDF)

2. **Module de feature engineering**
   - Agrégations pour chaque table secondaire (bureau, previous_application, etc.)
   - Jointures optimisées sur SK_ID_CURR
   - Création de features métier pertinentes :
     - Ratios financiers
     - Historiques de comportement
     - Features temporelles
     - Encodage des variables catégorielles
   - Au minimum 100+ features créées
   - Documentation des features (nom, description, type, distribution)

3. **Optimisation du stockage**
   - Conversion en format Parquet avec compression (Snappy ou GZIP)
   - Partitionnement des données si pertinent
   - Réduction de la taille sur disque (objectif : -70% vs CSV)
   - Benchmarking des temps de lecture

4. **Tests de qualité**
   - Tests unitaires pour chaque fonction de transformation
   - Tests d'intégration pour le pipeline complet
   - Great Expectations ou Pydantic pour validation des schémas
   - Assertions sur les features (plages de valeurs, non-nullité)

5. **Versioning**
   - Versioning des datasets transformés (tags ou versions)
   - Métadonnées de chaque version (date, taille, nb features, hash)
   - Capacité à recharger une version spécifique

**Architecture du pipeline** :
```
Raw Data (CSV)
  → Validation & Quality Checks
  → Transformation & Feature Engineering
  → Optimized Storage (Parquet)
  → Feature Store
  → Model Training
```

**Compétences mobilisées** :
Pandas, Parquet, Great Expectations, Pydantic, data quality, optimisation I/O, feature engineering

**Critères de réussite** :
- Pipeline exécutable de bout en bout sans erreur
- Rapport de qualité généré automatiquement
- 100+ features créées et documentées
- Réduction de 70%+ de la taille des données
- Tests de qualité qui passent (>90% coverage)

---

### PARTIE 2 : Entraînement et optimisation ML

**Objectifs** :
- Entraîner et comparer plusieurs modèles de classification
- Optimiser les hyperparamètres du meilleur modèle
- Gérer le déséquilibre des classes
- Optimiser le seuil de décision selon un coût métier
- Configurer MLflow pour tracking et registry

**Livrables attendus** :

1. **Configuration MLflow**
   - MLflow Tracking Server avec backend PostgreSQL
   - Artifact store configuré (local ou cloud)
   - Connexion depuis les notebooks/scripts
   - Organisation en expériences logiques

2. **Entraînement de modèles baseline (minimum 5 modèles)**
   - Logistic Regression (baseline simple)
   - Random Forest
   - XGBoost
   - LightGBM
   - MLP (Neural Network)
   - Autres modèles au choix (CatBoost, SVM, etc.)

   Pour chaque modèle :
   - Gestion du déséquilibre (class_weight, scale_pos_weight, SMOTE)
   - Validation croisée stratifiée (5 folds minimum)
   - Logging dans MLflow (paramètres, métriques, modèle)
   - Temps d'entraînement tracé

3. **Métriques et évaluation**

   **Métriques techniques** :
   - AUC-ROC (objectif : >0.75)
   - Accuracy
   - Precision, Recall, F1-Score
   - Confusion Matrix
   - Courbe ROC
   - Courbe Precision-Recall

   **Métriques métier** :
   - Coût d'erreur = 10 × FN + 1 × FP (hypothèse : un faux négatif coûte 10x plus cher)
   - Fonction de coût à minimiser
   - ROI estimé
   - Taux d'acceptation de crédit

4. **Optimisation des hyperparamètres**
   - Sélection du meilleur modèle baseline (selon coût métier)
   - Optimisation avec Optuna ou GridSearchCV
   - Minimum 50 trials pour l'optimisation
   - Recherche sur espace large de paramètres :
     - Profondeur d'arbres
     - Learning rate
     - Nombre d'estimateurs
     - Regularization
     - Etc.
   - Tracking de toutes les expérimentations dans MLflow

5. **Optimisation du seuil de décision**
   - Analyse du trade-off FN vs FP
   - Calcul du coût métier pour seuils de 0.1 à 0.9 (pas de 0.05)
   - Graphique coût vs seuil
   - Sélection du seuil optimal (minimise le coût métier)
   - Documentation de la décision

6. **Model Registry**
   - Enregistrement du meilleur modèle dans MLflow Registry
   - Versioning du modèle
   - Tags et métadonnées (métriques, seuil optimal, date)
   - Transition vers stage "Staging"

**Comparaison des modèles** :
Tableau récapitulatif avec :
- Nom du modèle
- AUC-ROC
- Coût métier (au seuil optimal)
- Seuil optimal
- Temps d'entraînement
- Décision (sélectionné ou non)

**Compétences mobilisées** :
MLflow, Scikit-learn, XGBoost, LightGBM, Optuna, gestion du déséquilibre, optimisation métier, validation croisée

**Critères de réussite** :
- Au moins 5 modèles entraînés et comparés
- Optimisation des hyperparamètres effectuée
- Seuil de décision optimisé selon coût métier
- AUC-ROC > 0.75 sur le meilleur modèle
- Toutes les expérimentations trackées dans MLflow
- Modèle final dans Model Registry

---

### PARTIE 3 : Interprétabilité et analyse

**Objectifs** :
- Comprendre les décisions du modèle
- Identifier les features les plus importantes
- Générer des explications locales pour des clients spécifiques
- Assurer la conformité et la transparence

**Livrables attendus** :

1. **Feature Importance globale**
   - Importance native du modèle (feature_importances_)
   - Top 30 features les plus importantes
   - Visualisation (bar plot)
   - Export CSV pour documentation

2. **Analyse SHAP**

   **SHAP global** :
   - SHAP summary plot (distribution des impacts)
   - SHAP importance plot (moyenne des valeurs absolues)
   - Identification des features clés
   - Compréhension des patterns globaux

   **SHAP local** :
   - Waterfall plot pour au moins 2 clients :
     - 1 client prédit en défaut (TARGET=1)
     - 1 bon client (TARGET=0)
   - Explication détaillée de chaque prédiction
   - Documentation de la démarche d'explication

3. **Documentation de l'interprétabilité**
   - Rapport d'interprétabilité (markdown ou PDF)
   - Justification de la sélection des features
   - Explication des décisions pour conformité RGPD
   - Guidelines pour expliquer un score à un chargé d'études

**Compétences mobilisées** :
SHAP, interprétabilité ML, visualisation, conformité, documentation

**Critères de réussite** :
- Feature importance calculée et visualisée
- Analyse SHAP globale complète
- Au moins 2 explications locales détaillées
- Rapport d'interprétabilité rédigé

---

### PARTIE 4 : Containerisation et Infrastructure

**Objectifs** :
- Dockeriser l'ensemble de la plateforme
- Créer une infrastructure locale reproductible
- Orchestrer les services avec Docker Compose
- Automatiser les builds

**Livrables attendus** :

1. **Dockerfiles pour chaque composant**

   À créer (exemples de composants) :
   - **Dockerfile.etl** : Pipeline ETL
   - **Dockerfile.training** : Entraînement des modèles
   - **Dockerfile.api** : API de prédiction (FastAPI)
   - **Dockerfile.mlflow** : MLflow Server

   Exigences :
   - Multi-stage builds pour réduire la taille
   - Optimisation du caching des layers
   - .dockerignore configuré
   - Images < 1GB si possible
   - Security best practices (non-root user, minimal base image)

2. **Docker Compose pour orchestration locale**

   Services à orchestrer :
   - PostgreSQL (backend MLflow)
   - MLflow Server
   - API de prédiction
   - (optionnel) Jupyter pour exploration

   Exigences :
   - Networking correct entre services
   - Volumes pour persistance des données
   - Variables d'environnement pour configuration
   - Healthchecks
   - Restart policies

3. **Scripts d'automatisation**
   - Script de build de toutes les images
   - Script de déploiement local (docker-compose up)
   - Script de tests d'intégration
   - Script de cleanup

4. **Tests d'intégration Docker**
   - docker-compose.test.yml pour tests isolés
   - Tests automatisés du pipeline complet
   - Validation des endpoints API
   - Cleanup automatique après tests

**Compétences mobilisées** :
Docker, Docker Compose, multi-stage builds, networking, volumes, orchestration

**Critères de réussite** :
- Tous les composants dockerisés
- docker-compose up démarre la plateforme complète
- Images optimisées (<1GB)
- Tests d'intégration passent
- Documentation Docker complète

---

### PARTIE 5 : Déploiement Kubernetes

**Objectifs** :
- Déployer la plateforme sur Kubernetes
- Implémenter scaling et haute disponibilité
- Gérer les secrets et configurations
- Créer un Helm chart réutilisable

**Livrables attendus** :

1. **Setup Kubernetes local**
   - Minikube, kind ou Docker Desktop
   - Configuration kubectl
   - Namespace dédié (mlops-credit-scoring)

2. **Manifests Kubernetes**

   À créer pour chaque service :
   - **Deployments** (postgres, mlflow, api)
   - **Services** (ClusterIP, LoadBalancer)
   - **ConfigMaps** (configuration non-sensible)
   - **Secrets** (credentials DB, API keys)
   - **PersistentVolumeClaims** (stockage PostgreSQL)
   - **Ingress** (routing, noms de domaine)
   - **HorizontalPodAutoscaler** (auto-scaling API)

   Exigences :
   - Replicas multiples pour HA (API : 3 replicas minimum)
   - Liveness et readiness probes
   - Resource requests et limits
   - Labels et selectors cohérents
   - Annotations pour documentation

3. **Helm Chart**

   Structure :
   - Chart.yaml (metadata)
   - values.yaml (valeurs par défaut)
   - values-dev.yaml (environnement dev)
   - values-staging.yaml (environnement staging)
   - values-prod.yaml (environnement production)
   - templates/ (manifests templatisés)

   Fonctionnalités :
   - Paramétrage de l'image (tag, registry)
   - Paramétrage des replicas
   - Paramétrage des resources
   - Activation/désactivation de composants
   - Multi-environnement

4. **Auto-scaling**
   - HPA configuré sur l'API
   - Scaling basé sur CPU (seuil : 70%)
   - Min replicas : 3, Max replicas : 10
   - Tests de charge pour valider le scaling

5. **Gestion des secrets**
   - Secrets Kubernetes pour passwords
   - Pas de secrets en clair dans les fichiers
   - Documentation de la création des secrets
   - (optionnel) External Secrets Operator ou Sealed Secrets

**Compétences mobilisées** :
Kubernetes, Helm, kubectl, manifests YAML, auto-scaling, ingress, secrets management

**Critères de réussite** :
- Plateforme déployée sur K8s
- Helm chart fonctionnel
- Auto-scaling validé par tests de charge
- Secrets correctement gérés
- Accès externe via Ingress
- Documentation K8s complète

---

### PARTIE 6 : CI/CD et Automatisation

**Objectifs** :
- Créer une pipeline CI/CD complète
- Automatiser tests et déploiement
- Implémenter GitOps
- Gérer des releases versionnées

**Livrables attendus** :

1. **Pipeline CI (Continuous Integration)**

   À automatiser (sur chaque push/PR) :
   - **Linting** : Flake8, Black, MyPy
   - **Tests unitaires** : Pytest avec coverage (>80%)
   - **Tests d'intégration** : Tests du pipeline ETL
   - **Security scan** : Trivy ou Snyk
   - **Build Docker images** : Build et tag
   - **Upload coverage** : Codecov ou Coveralls

   Outils : GitHub Actions, GitLab CI ou Cloud Build (GCP)

2. **Pipeline CD (Continuous Deployment)**

   À automatiser (sur tag de version) :
   - **Build et push images** : Vers GitHub Container Registry ou Artifact Registry (GCP)
   - **Déploiement staging** : Automatique
   - **Smoke tests staging** : Validation post-déploiement
   - **Déploiement production** : Avec approbation manuelle
   - **Rollback** : En cas d'échec

   Stratégie de déploiement :
   - Rolling update pour zero-downtime
   - Blue/Green ou Canary (bonus)

3. **Multi-environnements**
   - **Dev** : Local ou cluster dev
   - **Staging** : Pré-production
   - **Production** : Environnement final

   Différences :
   - Replicas (dev: 1, staging: 2, prod: 3+)
   - Resources (limits différents)
   - Configurations (features flags)

4. **Tests automatisés**

   **Tests unitaires** (tests/unit/) :
   - Tests des fonctions ETL
   - Tests des transformations
   - Tests de la logique métier
   - Coverage >80%

   **Tests d'intégration** (tests/integration/) :
   - Test du pipeline complet
   - Test de l'entraînement
   - Test de l'API avec mock model

   **Tests e2e** (tests/e2e/) :
   - Test de l'endpoint /predict
   - Test de l'endpoint /health
   - Test de performance (latence)

5. **Pre-commit hooks**
   - Black (formatting)
   - Flake8 (linting)
   - MyPy (type checking)
   - Tests rapides
   - Prévention de commit de secrets

6. **Versioning et releases**
   - Semantic versioning (v1.0.0, v1.1.0, etc.)
   - Tags Git pour releases
   - Changelog automatique
   - Release notes

**Compétences mobilisées** :
GitHub Actions, GitLab CI, pytest, Docker, Helm, GitOps, testing, versioning

**Critères de réussite** :
- Pipeline CI qui passe sur chaque commit
- Pipeline CD déploie automatiquement en staging
- Tests >80% coverage
- Déploiement multi-environnements fonctionnel
- Pre-commit hooks configurés
- Documentation CI/CD complète

---

### PARTIE 7 : Orchestration avec Apache Airflow

**Objectifs** :
- Orchestrer le pipeline ML complet avec Airflow
- Automatiser le ré-entraînement périodique
- Gérer les dépendances entre tâches
- Monitoring des workflows

**Livrables attendus** :

1. **Setup Apache Airflow**

   Options :
   - Airflow local avec Docker Compose
   - Cloud Composer sur GCP (si GCP est utilisé)

   Composants :
   - Airflow Webserver
   - Airflow Scheduler
   - PostgreSQL (metadata database)
   - (optionnel) Celery workers pour parallélisation

2. **DAG pour pipeline ML complet**

   Tâches à orchestrer (ordre logique) :
   1. **Vérification des données** : Nouvelle data disponible ?
   2. **Ingestion** : Chargement des fichiers CSV
   3. **Validation** : Data quality checks
   4. **Transformation** : Feature engineering
   5. **Entraînement** : Train multiple models
   6. **Évaluation** : Compare models et sélection
   7. **Tests modèle** : Validation du modèle
   8. **Promotion** : Staging dans MLflow Registry
   9. **Déploiement** : Rolling update K8s
   10. **Vérification** : Smoke tests post-déploiement

   Exigences :
   - DAG avec dépendances claires
   - Retry logic (2-3 retries)
   - Timeout sur les tâches longues
   - Alerting en cas d'échec (email ou Slack)
   - Schedule : Hebdomadaire ou mensuel
   - Tags pour organisation

3. **DAG pour monitoring et drift detection**

   Tâches :
   1. **Détection drift données** : Evidently AI sur nouvelles données
   2. **Détection drift modèle** : Performance vs baseline
   3. **Alerting** : Notification si drift détecté
   4. **Rapport** : Génération de rapport HTML

   Schedule : Quotidien

4. **Custom Operators (optionnel mais recommandé)**
   - MLflowModelPromotionOperator (promotion Staging → Production)
   - DataQualityCheckOperator (validation Great Expectations)
   - ModelServingUpdateOperator (update déploiement K8s)

5. **Monitoring Airflow**
   - Intégration avec Prometheus (métriques DAG)
   - Alertes sur échecs de DAG
   - Dashboards Grafana pour Airflow
   - SLA monitoring

**Compétences mobilisées** :
Apache Airflow, DAGs, operators, scheduling, orchestration, monitoring workflows

**Critères de réussite** :
- DAG ML pipeline fonctionnel et testé
- DAG drift detection actif
- Scheduling configuré
- Alerting en cas d'échec
- Monitoring Airflow opérationnel
- Documentation Airflow complète

---

### PARTIE 8 : Observabilité et Monitoring

**Objectifs** :
- Implémenter une stack de monitoring complète
- Centraliser les logs
- Créer des dashboards métier et techniques
- Mettre en place des alertes intelligentes

**Livrables attendus** :

1. **Stack de monitoring**

   Options :
   - **Open Source** : Prometheus + Grafana + Alertmanager
   - **GCP** : Cloud Monitoring + Cloud Logging

   Composants (si open source) :
   - Prometheus (métriques)
   - Grafana (dashboards)
   - Node Exporter (métriques système)
   - cAdvisor (métriques containers)
   - Alertmanager (alerting)

2. **Instrumentation de l'API**

   Métriques à exposer :
   - **Métriques HTTP** :
     - Nombre de requêtes (/predict, /health)
     - Latence (p50, p95, p99)
     - Taux d'erreur (4xx, 5xx)
   - **Métriques métier** :
     - Nombre de prédictions
     - Distribution des scores (0-1)
     - % de crédits acceptés/refusés
     - Version du modèle actif
   - **Métriques système** :
     - CPU, Memory
     - Temps de réponse du modèle

   Outil : prometheus_client ou OpenTelemetry

3. **Dashboards Grafana** (ou Cloud Monitoring)

   À créer (minimum 3 dashboards) :

   **Dashboard API** :
   - Requêtes par seconde
   - Latence p50, p95, p99
   - Taux d'erreur
   - Uptime

   **Dashboard Modèle** :
   - Nombre de prédictions
   - Distribution des scores
   - % acceptation crédit
   - Version modèle
   - Drift score

   **Dashboard Infrastructure** :
   - CPU/Memory par pod
   - Network I/O
   - Disk usage
   - Pod count et autoscaling
   - Database connections

4. **Alerting**

   Règles d'alerte à configurer :
   - **Critique** :
     - API down (>5min)
     - Taux d'erreur >5% (>5min)
     - Database connection lost
   - **Warning** :
     - Latence p95 >1s (>10min)
     - CPU >80% (>15min)
     - Drift score >0.5 (>1h)
     - Disk >85%

   Canaux d'alerte :
   - Email
   - Slack (bonus)
   - PagerDuty (bonus)

5. **Drift Detection**

   Avec Evidently AI :
   - **Data Drift** : Distribution des features vs reference
   - **Model Drift** : Performance du modèle vs baseline
   - **Target Drift** : Distribution de la cible

   Fonctionnalités :
   - Génération de rapports HTML automatiques
   - Métriques de drift exposées à Prometheus
   - Alertes si drift significatif
   - Dashboard dédié

6. **Logs centralisés (optionnel)**

   Stack ELK ou Cloud Logging :
   - Elasticsearch (stockage)
   - Logstash (ingestion)
   - Kibana (visualisation)

   Logs à centraliser :
   - Logs API
   - Logs MLflow
   - Logs Airflow
   - Logs Kubernetes

**Compétences mobilisées** :
Prometheus, Grafana, Evidently AI, alerting, observabilité, drift detection, dashboards

**Critères de réussite** :
- Stack de monitoring déployée
- Au moins 3 dashboards créés
- Alerting configuré et testé
- Drift detection active
- Métriques API exposées
- Documentation monitoring complète

---

## API DE PRÉDICTION (FastAPI)

**Endpoints requis** :

1. **POST /predict**
   - Input : Données client (JSON)
   - Output : Score de risque (0-1), décision (accepté/refusé), version modèle
   - Latence : <200ms (p95)

2. **GET /health**
   - Output : Status (healthy/unhealthy), version API

3. **GET /metrics**
   - Output : Métriques Prometheus (format texte)

4. **GET /model-info**
   - Output : Version modèle, date de déploiement, métriques d'entraînement

**Exigences** :
- Validation des inputs (Pydantic)
- Logging de chaque requête
- Gestion d'erreurs robuste
- Documentation Swagger automatique
- Tests unitaires et d'intégration

---

## RÉSULTATS ATTENDUS

### Infrastructure
- Plateforme MLOps complète déployée sur Kubernetes
- Auto-scaling fonctionnel (3-10 pods)
- Pipeline CI/CD automatisée (dev → staging → prod)
- Orchestration Airflow avec DAGs opérationnels
- Stack de monitoring avec dashboards et alertes

### Machine Learning
- 5+ modèles entraînés et comparés
- Optimisation hyperparamètres effectuée
- Seuil de décision optimisé selon coût métier
- AUC-ROC >0.75 sur le meilleur modèle
- Interprétabilité complète (SHAP)
- Model Registry avec versioning

### Data Engineering
- Pipeline ETL scalable traite 2.5GB en <1h
- 100+ features créées et documentées
- Data quality checks automatiques
- Stockage optimisé (Parquet, -70% taille)
- Versioning des données

### Qualité
- Tests >80% coverage
- Tests automatisés (unit, intégration, e2e)
- Linting et formatage (Black, Flake8)
- Pre-commit hooks configurés
- Security scans passent

### Performance
- API latence <200ms (p95)
- Disponibilité >99% (uptime)
- Auto-scaling validé par tests de charge
- Zero-downtime deployments

### Documentation
- Architecture complète documentée
- README avec instructions de déploiement
- Documentation API (Swagger)
- Runbooks pour opérations courantes
- Documentation des décisions techniques

---

## LIVRABLES FINAUX

### Code

Tous les livrables doivent être versionnés sur un repository Git :

1. **src/** : Code source
   - data_ingestion.py
   - feature_engineering.py
   - train.py
   - drift_detection.py
   - api/main.py

2. **tests/** : Tests automatisés
   - unit/
   - integration/
   - e2e/

3. **k8s/** : Manifests Kubernetes
   - deployments/
   - services/
   - configmaps/
   - secrets/
   - ingress/
   - hpa/

4. **helm/** : Helm chart
   - Chart.yaml
   - values*.yaml
   - templates/

5. **airflow/** : DAGs Airflow
   - dags/
   - plugins/

6. **monitoring/** : Configuration monitoring
   - prometheus.yml
   - grafana/dashboards/
   - alerts.yml

7. **.github/workflows/** : Pipelines CI/CD
   - ci.yml
   - cd.yml

8. **docker-compose.yml** : Orchestration locale

9. **Dockerfiles** : Un par service

10. **requirements.txt** : Dépendances Python

### Documentation

1. **README.md** :
   - Description du projet
   - Instructions d'installation
   - Guide de démarrage rapide
   - Architecture overview

2. **docs/ARCHITECTURE.md** :
   - Diagramme d'architecture complet
   - Description de chaque composant
   - Flux de données

3. **docs/DEPLOYMENT.md** :
   - Guide de déploiement complet
   - Prérequis
   - Commandes étape par étape
   - Troubleshooting

4. **docs/API.md** :
   - Documentation des endpoints
   - Exemples de requêtes
   - Codes d'erreur

5. **docs/MONITORING.md** :
   - Description des dashboards
   - Liste des alertes
   - Procédures d'incident

6. **docs/ML_MODEL.md** :
   - Description du modèle final
   - Métriques de performance
   - Interprétabilité
   - Décisions techniques

### Visualisations

1. Comparaison des modèles (bar chart)
2. Courbes ROC pour chaque modèle
3. Graphique coût métier vs seuil
4. Feature importance (top 30)
5. SHAP summary plot
6. SHAP waterfall (2 exemples)
7. Dashboards Grafana (export PNG/JSON)
8. Architecture diagram

### Fichiers de résultats

1. models_comparison.csv
2. feature_importance.csv
3. data_quality_report.html
4. shap_report.html

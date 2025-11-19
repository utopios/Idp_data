# TP BigQuery ML - Prédiction et déploiement externe

## Contexte du TP

Vous allez construire un modèle de prédiction sur des données publiques de vélos en libre-service de Londres, l'entraîner dans BigQuery ML, puis le déployer en dehors de BigQuery pour l'utiliser dans une application Python.

**Durée estimée :** 

**Prérequis :**
- Compte GCP avec billing activé
- Connaissance SQL de base
- Python 3.8+

---

## Partie 1 : Exploration des données

### 1.1 Connexion au dataset public

Connectez-vous à votre projet BigQuery et explorez le dataset `bigquery-public-data.london_bicycles.cycle_hire`.

**Questions à résoudre :**
- Combien de trajets sont enregistrés ? ()
- Quelle est la période couverte ?
- Quelles sont les stations les plus utilisées ?

```sql
SELECT 
  COUNT(*) as total_trips,
  MIN(start_date) as first_trip,
  MAX(end_date) as last_trip
FROM `bigquery-public-data.london_bicycles.cycle_hire`
```

```sql
SELECT
  start_station_name,
  COUNT(*) as trip_count,
  ROUND(AVG(duration), 2) as avg_duration_seconds
FROM `bigquery-public-data.london_bicycles.cycle_hire`
WHERE start_station_name IS NOT NULL
GROUP BY start_station_name
ORDER BY trip_count DESC
LIMIT 20;
```


### 1.2 Analyse exploratoire

Créez des requêtes pour identifier :
- La distribution des durées de trajet
- Les patterns temporels (heure, jour de la semaine)
- Les corrélations entre stations de départ et d'arrivée

---

## Partie 2 : Préparation des données

### 2.1 Création d'un dataset de travail

Créez un dataset dans votre projet pour stocker vos tables intermédiaires.

### 2.2 Feature engineering

Construisez une table d'entraînement avec ces features :
- Extraction des composantes temporelles (heure, jour de la semaine, mois)
- Calcul de la distance entre stations (si coordonnées disponibles)
- Agrégation du nombre de trajets par station
- Variables météo (si vous joignez avec `bigquery-public-data.noaa_gsod`)

**Objectif :** Prédire la durée d'un trajet en fonction des caractéristiques extraites.

### 2.3 Split train/test

Divisez vos données en ensembles d'entraînement (80%) et de test (20%).

---

## Partie 3 : Entraînement du modèle BigQuery ML 

### 3.1 Création du modèle de régression

Utilisez `CREATE MODEL` pour entraîner un modèle de régression linéaire :

```sql
CREATE OR REPLACE MODEL `votre_projet.votre_dataset.bike_duration_model`
OPTIONS(
  model_type='linear_reg',
  input_label_cols=['duration'],
  data_split_method='seq',
  data_split_col='start_date'
) AS
SELECT
  -- vos features
  duration
FROM `votre_table_features`
```

### 3.2 Évaluation du modèle

Utilisez `ML.EVALUATE` pour obtenir les métriques de performance :
- RMSE
- R²
- MAE

Testez également un modèle boosted tree et comparez les performances.

### 3.3 Prédictions dans BigQuery

Utilisez `ML.PREDICT` pour générer des prédictions sur votre ensemble de test.

---

## Partie 4 : Export du modèle 

### 4.1 Export vers Google Cloud Storage

Exportez votre modèle entraîné :

```sql
EXPORT MODEL `votre_projet.votre_dataset.bike_duration_model`
OPTIONS(URI='gs://votre-bucket/models/bike_model')
```

### 4.2 Téléchargement en local

Utilisez gsutil pour télécharger le modèle sur votre machine locale :

```bash
gsutil -m cp -r gs://votre-bucket/models/bike_model ./local_model
```

---

## Partie 5 : Déploiement et utilisation externe

### 5.1 Chargement du modèle avec TensorFlow

Installez les dépendances nécessaires :

```bash
pip install tensorflow google-cloud-bigquery pandas
```

Chargez et utilisez le modèle en Python :

```python
import tensorflow as tf
import pandas as pd

# Charger le modèle
model = tf.saved_model.load('./local_model')

# Préparer des données de test
test_data = pd.DataFrame({
    'hour': [8, 14, 18],
    'day_of_week': [1, 3, 5],
    # autres features...
})

# Faire des prédictions
predictions = model(test_data)
```

### 5.2 Création d'une API Flask

Créez une API simple pour servir les prédictions :

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Preprocessing
    # Prédiction
    # Retour JSON
    return jsonify({'predicted_duration': result})
```

### 5.3 Tests et validation

Comparez les prédictions de votre API avec celles de BigQuery ML.PREDICT pour valider la cohérence.

---

## Livrables attendus

1. Script SQL complet de préparation des données
2. Modèles entraînés (au moins 2 types différents)
3. Rapport d'évaluation des performances
4. Code Python de déploiement
5. Documentation de l'API

## Points bonus

- Déploiement sur Cloud Run ou Vertex AI
- Ajout de monitoring des prédictions
- Pipeline automatisé avec Airflow ou Cloud Composer

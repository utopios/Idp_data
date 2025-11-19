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

SELECT
  CASE
    WHEN duration < 300 THEN '0-5 min'
    WHEN duration < 600 THEN '5-10 min'
    WHEN duration < 900 THEN '10-15 min'
    WHEN duration < 1200 THEN '15-20 min'
    WHEN duration < 1800 THEN '20-30 min'
    WHEN duration < 3600 THEN '30-60 min'
    ELSE '60+ min'
  END as duration_bucket,
  COUNT(*) as trip_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM `bigquery-public-data.london_bicycles.cycle_hire`
WHERE duration IS NOT NULL
  AND duration > 0
  AND duration < 86400  
GROUP BY duration_bucket
ORDER BY
  CASE
    WHEN duration_bucket = '0-5 min' THEN 1
    WHEN duration_bucket = '5-10 min' THEN 2
    WHEN duration_bucket = '10-15 min' THEN 3
    WHEN duration_bucket = '15-20 min' THEN 4
    WHEN duration_bucket = '20-30 min' THEN 5
    WHEN duration_bucket = '30-60 min' THEN 6
    ELSE 7
  END;


- Les patterns temporels (heure, jour de la semaine)

SELECT
  EXTRACT(HOUR FROM start_date) as hour,
  COUNT(*) as trip_count,
  ROUND(AVG(duration), 2) as avg_duration_seconds
FROM `bigquery-public-data.london_bicycles.cycle_hire`
WHERE start_date IS NOT NULL
GROUP BY hour
ORDER BY trip_count DESC;

- Les corrélations entre stations de départ et d'arrivée

SELECT
  start_station_name,
  end_station_name,
  COUNT(*) as trip_count,
  ROUND(AVG(duration), 2) as avg_duration
FROM `bigquery-public-data.london_bicycles.cycle_hire`
WHERE start_station_name IS NOT NULL
  AND end_station_name IS NOT NULL
  AND start_station_name != end_station_name
GROUP BY start_station_name, end_station_name
ORDER BY trip_count DESC
LIMIT 10;

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

```sql

CREATE SCHEMA bike_ml_dataset
OPTIONS (
  location='EU'
);
CREATE OR REPLACE TABLE `bike_ml_dataset.bike_features` AS
WITH cleaned_data AS (
  SELECT
    rental_id,
    duration,
    bike_id,
    end_station_id,
    end_station_name,
    start_date,
    start_station_id,
    start_station_name,
    end_date
  FROM `bigquery-public-data.london_bicycles.cycle_hire`
  WHERE
    -- Filtrer les données aberrantes
    duration IS NOT NULL
    AND duration > 60           
    AND duration < 7200         
    AND start_date IS NOT NULL
    AND end_date IS NOT NULL
    AND start_station_id IS NOT NULL
    AND end_station_id IS NOT NULL
    AND start_date >= '2015-01-01'
),

station_stats AS (
  SELECT
    start_station_id,
    COUNT(*) as station_trip_count,
    AVG(duration) as station_avg_duration
  FROM cleaned_data
  GROUP BY start_station_id
)

SELECT
  -- Identifiant
  c.rental_id,

  -- Variable cible
  c.duration,

  -- Features temporelles
  EXTRACT(HOUR FROM c.start_date) as start_hour,
  EXTRACT(DAYOFWEEK FROM c.start_date) as day_of_week,
  EXTRACT(MONTH FROM c.start_date) as month,
  EXTRACT(YEAR FROM c.start_date) as year,
  EXTRACT(DAYOFYEAR FROM c.start_date) as day_of_year,

  -- Features booléennes pour segments temporels
  CASE WHEN EXTRACT(DAYOFWEEK FROM c.start_date) IN (1, 7) THEN 1 ELSE 0 END as is_weekend,
  CASE WHEN EXTRACT(HOUR FROM c.start_date) BETWEEN 7 AND 9 THEN 1 ELSE 0 END as is_morning_rush,
  CASE WHEN EXTRACT(HOUR FROM c.start_date) BETWEEN 17 AND 19 THEN 1 ELSE 0 END as is_evening_rush,

  -- Features stations
  c.start_station_id,
  c.end_station_id,
  CASE WHEN c.start_station_id = c.end_station_id THEN 1 ELSE 0 END as is_round_trip,

  -- Features statistiques des stations
  COALESCE(s.station_trip_count, 0) as start_station_popularity,
  COALESCE(s.station_avg_duration, 0) as start_station_avg_duration,

  -- Date pour le split
  c.start_date,

  -- Hash pour split aléatoire reproductible
  MOD(ABS(FARM_FINGERPRINT(CAST(c.rental_id AS STRING))), 100) as random_split

FROM cleaned_data c
LEFT JOIN station_stats s ON c.start_station_id = s.start_station_id;

SELECT
  start_hour,
  COUNT(*) as count,
  ROUND(AVG(duration), 2) as avg_duration
FROM `bike_ml_dataset.bike_features`
GROUP BY start_hour
ORDER BY start_hour;

```


**Objectif :** Prédire la durée d'un trajet en fonction des caractéristiques extraites.

### 2.3 Split train/test

Divisez vos données en ensembles d'entraînement (80%) et de test (20%).

```sql
CREATE OR REPLACE TABLE `bike_ml_dataset.bike_train` AS
SELECT
  duration,
  start_hour,
  day_of_week,
  month,
  is_weekend,
  is_morning_rush,
  is_evening_rush,
  is_round_trip,
  start_station_popularity,
  start_station_avg_duration,
  start_date
FROM `bike_ml_dataset.bike_features`
WHERE random_split < 80;

CREATE OR REPLACE TABLE `bike_ml_dataset.bike_test` AS
SELECT
  rental_id,
  duration,
  start_hour,
  day_of_week,
  month,
  is_weekend,
  is_morning_rush,
  is_evening_rush,
  is_round_trip,
  start_station_popularity,
  start_station_avg_duration,
  start_date
FROM `bike_ml_dataset.bike_features`
WHERE random_split >= 80;
```

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


CREATE OR REPLACE MODEL `bike_ml_dataset.bike_duration_linear_model`
OPTIONS(
  model_type='LINEAR_REG',
  input_label_cols=['duration'],
  data_split_method='SEQ',
  data_split_col='start_date',
  ls_init_learn_rate=0.1,
  l1_reg=0.0,
  l2_reg=0.0,
  max_iterations=50
) AS
SELECT
  duration,
  start_hour,
  day_of_week,
  month,
  is_weekend,
  is_morning_rush,
  is_evening_rush,
  is_round_trip,
  start_station_popularity,
  start_station_avg_duration,
  start_date
FROM `bike_ml_dataset.bike_train`;

SELECT
  *
FROM ML.EVALUATE(
  MODEL `bike_ml_dataset.bike_duration_linear_model`,
  (
    SELECT
      duration,
      start_hour,
      day_of_week,
      month,
      is_weekend,
      is_morning_rush,
      is_evening_rush,
      is_round_trip,
      start_station_popularity,
      start_station_avg_duration,
      start_date
    FROM `bike_ml_dataset.bike_test`
  )
);

SELECT
  *
FROM ML.TRAINING_INFO(MODEL `bike_ml_dataset.bike_duration_linear_model`)
ORDER BY iteration;

SELECT
  *
FROM ML.WEIGHTS(MODEL `bike_ml_dataset.bike_duration_linear_model`)
ORDER BY ABS(weight) DESC;

CREATE OR REPLACE MODEL `bike_ml_dataset.bike_duration_boosted_tree_model`
OPTIONS(
  model_type='BOOSTED_TREE_REGRESSOR',
  input_label_cols=['duration'],
  data_split_method='SEQ',
  data_split_col='start_date',
  max_iterations=50,
  learn_rate=0.1,
  min_tree_child_weight=10,
  subsample=0.8,
  max_tree_depth=6,
  early_stop=TRUE,
  min_rel_progress=0.01
) AS
SELECT
  duration,
  start_hour,
  day_of_week,
  month,
  is_weekend,
  is_morning_rush,
  is_evening_rush,
  is_round_trip,
  start_station_popularity,
  start_station_avg_duration,
  start_date
FROM `bike_ml_dataset.bike_train`;


SELECT
  *
FROM ML.EVALUATE(
  MODEL `bike_ml_dataset.bike_duration_boosted_tree_model`,
  (
    SELECT
      duration,
      start_hour,
      day_of_week,
      month,
      is_weekend,
      is_morning_rush,
      is_evening_rush,
      is_round_trip,
      start_station_popularity,
      start_station_avg_duration,
      start_date
    FROM `bike_ml_dataset.bike_test`
  )
);
```

### 3.2 Évaluation du modèle

Utilisez `ML.EVALUATE` pour obtenir les métriques de performance :
- RMSE
- R²
- MAE

Testez également un modèle boosted tree et comparez les performances.

### 3.3 Prédictions dans BigQuery

Utilisez `ML.PREDICT` pour générer des prédictions sur votre ensemble de test.

```sql

CREATE OR REPLACE TABLE `bike_ml_dataset.predictions` AS
SELECT
  rental_id,
  duration as actual_duration,
  predicted_duration,
  ABS(duration - predicted_duration) as absolute_error,
  ROUND(ABS(duration - predicted_duration) / duration * 100, 2) as percentage_error
FROM ML.PREDICT(
  MODEL `bike_ml_dataset.bike_duration_boosted_tree_model`,
  (SELECT * FROM `bike_ml_dataset.bike_test`)
);

SELECT
  *
FROM ML.PREDICT(
  MODEL `bike_ml_dataset.bike_duration_boosted_tree_model`,
  (
    SELECT
      8 as start_hour,
      2 as day_of_week,
      6 as month,
      0 as is_weekend,
      1 as is_morning_rush,
      0 as is_evening_rush,
      0 as is_round_trip,
      5000 as start_station_popularity,
      900 as start_station_avg_duration,
      CURRENT_TIMESTAMP() as start_date
  )
);

```

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

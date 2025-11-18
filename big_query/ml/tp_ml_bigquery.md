# BigQuery ML - Analyse des Ventes d'Alcool en Iowa

Vous êtes Data Analyst pour **Iowa Liquor Board**, l'organisme qui régule la vente d'alcool dans l'État de l'Iowa (USA). 

Votre mission : analyser les données de ventes pour :
- Optimiser la gestion des stocks
- Identifier les zones à fort potentiel
- Segmenter les points de vente
- Prédire les ventes futures
- Détecter les produits à succès


**Table BigQuery** : `bigquery-public-data.iowa_liquor_sales.sales`

**Contenu** : Plus de 20 millions de transactions de ventes d'alcool (2012-2024)

**Colonnes principales** :
- `date` : Date de la vente
- `store_number` : ID du magasin
- `store_name` : Nom du magasin
- `address`, `city`, `zip_code`, `county` : Localisation
- `category`, `category_name` : Catégorie du produit
- `vendor_number`, `vendor_name` : Fournisseur
- `item_number`, `item_description` : Produit
- `pack`, `bottle_volume_ml` : Conditionnement
- `state_bottle_cost`, `state_bottle_retail` : Prix
- `bottles_sold` : Quantité vendue
- `sale_dollars` : Montant de la vente
- `volume_sold_liters`, `volume_sold_gallons` : Volume

## OBJECTIFS PÉDAGOGIQUES

1. Exploration et nettoyage de données
2. Régression linéaire (LINEAR_REG)
3. Classification (LOGISTIC_REG)
4. Clustering (KMEANS)
5. Arbres boostés (BOOSTED_TREE)
6. Réseaux de neurones (DNN)
7. AutoML
8. Comparaison et choix de modèles

---

## EXERCICE 1 : EXPLORATION DES DONNÉES 

### Objectif
Comprendre les données avant de modéliser.

### Tâches à réaliser

**1.1** Explorer la structure de la table
- Lister toutes les colonnes et leurs types
- Afficher 20 lignes d'exemple

**1.2** Statistiques descriptives
- Nombre total de transactions
- Période couverte (date min et max)
- Nombre de magasins uniques
- Nombre de produits différents
- Montant total des ventes
- Vente moyenne par transaction
- Top 10 des villes par nombre de magasins

**1.3** Analyses temporelles
- Ventes par année
- Ventes par mois (identifier la saisonnalité)
- Ventes par jour de la semaine

**1.4** Analyses par catégorie
- Top 10 des catégories de produits par CA
- Distribution des prix (min, max, moyenne, médiane)

**1.5** Identification des anomalies
- Transactions avec montant négatif ou nul
- Quantités aberrantes (> 10 000 bouteilles)
- Dates incohérentes

---

## EXERCICE 2 : RÉGRESSION LINÉAIRE - Prédire le Montant des Ventes 

### Objectif
Créer un modèle pour **prédire `sale_dollars`** (montant de la vente) en fonction des caractéristiques de la transaction.

### Tâches à réaliser

**2.1** Préparation des données
- Créer une table nettoyée avec seulement les données valides :
  - `sale_dollars` entre 10$ et 10 000$
  - `bottles_sold` entre 1 et 1 000
  - Date >= 2020 (données récentes)
  - Supprimer les valeurs NULL
- Limiter à 500 000 lignes pour commencer

**2.2** Modèle SIMPLE
- Créer un modèle LINEAR_REG avec uniquement :
  - `bottles_sold` (quantité)
  - `state_bottle_retail` (prix unitaire)
- Évaluer les performances (MAE, R²)
- Analyser les coefficients

**2.3** Modèle ENRICHI
- Ajouter des features :
  - Mois, jour de la semaine
  - Catégorie du produit
  - Volume de la bouteille
  - Ville
- Comparer avec le modèle simple

**2.4** Analyse
- Quelles variables sont les plus importantes ?
- Le modèle est-il meilleur que le simple calcul `prix × quantité` ?
- Sur quels types de transactions le modèle se trompe-t-il le plus ?

### Questions d'analyse
- Pourquoi le R² est-il probablement très élevé ?
- Y a-t-il une multicolinéarité évidente ?
- Comment améliorer le modèle ?
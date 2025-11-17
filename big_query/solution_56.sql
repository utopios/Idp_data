CREATE OR REPLACE TABLE `ihab_2.ventes_partitioned`
(
  id_vente INT64,
  date_vente DATE,
  id_produit INT64,
  nom_produit STRING,
  categorie STRING,
  quantite INT64,
  prix_unitaire FLOAT64,
  montant_total FLOAT64,
  region STRING,
  id_client INT64
)
PARTITION BY date_vente;

CREATE OR REPLACE TABLE `ihab_2.ventes_no_partitioned`
(
  id_vente INT64,
  date_vente DATE,
  id_produit INT64,
  nom_produit STRING,
  categorie STRING,
  quantite INT64,
  prix_unitaire FLOAT64,
  montant_total FLOAT64,
  region STRING,
  id_client INT64
);

INSERT INTO `ihab_2.ventes_partitioned`
SELECT
  ROW_NUMBER() OVER() as id_vente,
  DATE_ADD('2023-01-01', INTERVAL CAST(RAND() * 730 AS INT64) DAY) as date_vente,
  CAST(RAND() * 100 AS INT64) + 1 as id_produit,
  CONCAT('Produit_', CAST(CAST(RAND() * 100 AS INT64) + 1 AS STRING)) as nom_produit,
  CASE
    WHEN RAND() < 0.25 THEN 'Électronique'
    WHEN RAND() < 0.50 THEN 'Vêtements'
    WHEN RAND() < 0.75 THEN 'Alimentation'
    ELSE 'Maison'
  END as categorie,
  CAST(RAND() * 10 AS INT64) + 1 as quantite,
  ROUND(RAND() * 500 + 10, 2) as prix_unitaire,
  ROUND((RAND() * 10 + 1) * (RAND() * 500 + 10), 2) as montant_total,
  CASE
    WHEN RAND() < 0.20 THEN 'Nord'
    WHEN RAND() < 0.40 THEN 'Sud'
    WHEN RAND() < 0.60 THEN 'Est'
    WHEN RAND() < 0.80 THEN 'Ouest'
    ELSE 'Centre'
  END as region,
  CAST(RAND() * 1000 AS INT64) + 1 as id_client
FROM
  UNNEST(GENERATE_ARRAY(1, 1000000)) as n;


SELECT
  categorie,
  COUNT(*) as nb_ventes,
  SUM(montant_total) as total_ventes,
  AVG(montant_total) as moyenne_ventes
FROM
  `ihab_2.ventes_partitioned`
GROUP BY
  categorie
ORDER BY
  total_ventes DESC;


SELECT
  categorie,
  COUNT(*) as nb_ventes,
  SUM(montant_total) as total_ventes,
  AVG(montant_total) as moyenne_ventes
FROM
  `ihab_2.ventes_no_partitioned`
GROUP BY
  categorie
ORDER BY
  total_ventes DESC;


CREATE OR REPLACE TABLE `ihab_2.ventes_clustered`
(
  id_vente INT64,
  date_vente DATE,
  id_produit INT64,
  nom_produit STRING,
  categorie STRING,
  quantite INT64,
  prix_unitaire FLOAT64,
  montant_total FLOAT64,
  region STRING,
  id_client INT64
)
PARTITION BY date_vente
CLUSTER BY categorie, region
OPTIONS(
  description="Table partitionnée par date et clusterisée par catégorie et région"
);

-- Table partitionnée mais NON clusterisée (pour comparaison)
CREATE OR REPLACE TABLE `ihab_2.ventes_non_clustered`
(
  id_vente INT64,
  date_vente DATE,
  id_produit INT64,
  nom_produit STRING,
  categorie STRING,
  quantite INT64,
  prix_unitaire FLOAT64,
  montant_total FLOAT64,
  region STRING,
  id_client INT64
)
PARTITION BY date_vente
OPTIONS(
  description="Table partitionnée par date mais non clusterisée"
);

-- Insérer les données
INSERT INTO `ihab_2.ventes_clustered`
SELECT * FROM `ihab_2.ventes_partitioned`;

INSERT INTO `ihab_2.ventes_non_clustered`
SELECT * FROM `ihab_2.ventes_partitioned`;

CREATE MATERIALIZED VIEW `ihab_2.mv_ventes_quotidiennes`
PARTITION BY date_vente
CLUSTER BY categorie, region
OPTIONS(
  enable_refresh=true,
  refresh_interval_minutes=60,
  description="Vue matérialisée des ventes agrégées par jour"
)
AS
SELECT
  date_vente,
  categorie,
  region,
  COUNT(*) as nombre_ventes,
  COUNT(DISTINCT id_client) as nombre_clients,
  SUM(quantite) as quantite_totale,
  SUM(montant_total) as montant_total,
  AVG(montant_total) as montant_moyen,
  MIN(montant_total) as montant_min,
  MAX(montant_total) as montant_max,
  ROUND(STDDEV(montant_total), 2) as ecart_type_montant
FROM
  `ihab_2.ventes_clustered`
GROUP BY
  date_vente, categorie, region;


-- MV pour les tendances mensuelles par catégorie
CREATE MATERIALIZED VIEW `ihab_2.mv_ventes_mensuelles`
CLUSTER BY categorie
OPTIONS(
  enable_refresh=true,
  refresh_interval_minutes=120,
  description="Vue matérialisée des ventes mensuelles par catégorie"
)
AS
SELECT
  DATE_TRUNC(date_vente, MONTH) as mois,
  categorie,
  COUNT(*) as nombre_ventes,
  COUNT(DISTINCT id_client) as nombre_clients_uniques,
  COUNT(DISTINCT id_produit) as nombre_produits_differents,
  SUM(montant_total) as chiffre_affaires,
  ROUND(AVG(montant_total), 2) as panier_moyen,
  SUM(quantite) as quantite_totale
FROM
  `ihab_2.ventes_clustered`
GROUP BY
  mois, categorie;
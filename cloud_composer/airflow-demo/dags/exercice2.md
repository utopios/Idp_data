## Exercice 2 : Pipeline d’ingestion et de qualification de fichiers sur GCS


Chaque jour, un partenaire dépose un fichier CSV de ventes sur un bucket GCS :

* Bucket source : `raw-sales-bucket`
* Chemin des fichiers : `incoming/sales_YYYY-MM-DD.csv`

Tu dois construire un DAG Airflow qui :

1. Vérifie qu’un fichier pour la date d’exécution existe sur GCS.
2. Copie ce fichier depuis le bucket `raw` vers un bucket `staging`.
3. Lit le fichier depuis `staging` et applique des règles de qualité.
4. Partitionne les données en deux ensembles : lignes valides et lignes invalides.
5. Écrit deux nouveaux fichiers CSV sur GCS :

   * Bucket cible : `curated-sales-bucket`
   * `valid/processing_date=YYYY-MM-DD/sales_valid.csv`
   * `invalid/processing_date=YYYY-MM-DD/sales_invalid.csv`
6. Si le nombre de lignes invalides dépasse un seuil, déclenche une alerte (log ou tâche dédiée).

---

## Schéma du CSV sur GCS

Le fichier `sales_YYYY-MM-DD.csv` contient au minimum :

* `sale_id` (string, non vide)
* `customer_id` (string, non vide)
* `country` (string, ex: `FR`, `DE`, `US`)
* `amount` (float, > 0)
* `sale_ts` (timestamp ISO ou `YYYY-MM-DD HH:MM:SS`)

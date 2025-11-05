### Exercice 1: Organiser un Data Lake

**Objectif**: Créer une structure organisée dans GCS

1. Créer un bucket nommé `data-lake-[VOTRE_NOM]`
2. Créer la structure suivante:
   ```
   raw/
     ventes/
       2024/
         01/
         02/
     logs/
       2024/
         01/
   processed/
   archive/
   ```
3. Uploader les fichiers:
   - `ventes_2024_01.csv` dans `raw/ventes/2024/01/`
   - `ventes_2024_02.csv` dans `raw/ventes/2024/02/`
   - Les fichiers logs dans `raw/logs/2024/01/`

### Exercice 2: Script de Backup Local vers GCS

**Objectif**: Automatiser la sauvegarde de fichiers locaux

1. Créer un script Python `backup_to_gcs.py`
2. Le script doit:
   - Parcourir un dossier local (ex: ./data)
   - Compresser chaque fichier en .gz
   - Uploader vers GCS dans un dossier backup/YYYY-MM-DD/
   - Afficher une barre de progression (tqdm)
   - Logger les opérations dans backup.log

### Exercice 3: Conversion CSV vers Parquet

**Objectif**: Optimiser le stockage avec Parquet

1. Télécharger `transactions_1000.csv` depuis GCS
2. Lire avec Pandas
3. Convertir en format Parquet
4. Uploader le fichier Parquet dans GCS
5. Comparer les tailles:
   - Taille CSV
   - Taille Parquet
   - Ratio de compression

### Exercice 4 Pipeline ETL Simple

**Objectif**: Créer un pipeline complet de bout en bout

1. Extract: Télécharger des CSV depuis GCS
2. Transform: Nettoyer (supprimer lignes avec valeurs manquantes)
3. Load: Uploader les CSV nettoyés dans GCS

**Fichiers à utiliser**: data/ventes_invalides.csv
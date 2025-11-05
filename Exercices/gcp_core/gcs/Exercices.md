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
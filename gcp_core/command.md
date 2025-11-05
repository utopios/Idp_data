# Commande GCP

```bash
## Pour se connecter 
gcloud auth login

## Voir configuration
glcoud config list

## Voir les projets disponibles
gcloud projects list

## Voir le compte actif
glcoud auth list

## Créer des authentification pour des applications 
gcloud auth application-default login
```

## Commande cloud storage

```bash
# pour intéraction avec gcs
gsutil ls

# Commande pour copier un fichier 
gsutil cp data/data.csv gs://ihab_bucket_utopios/
# Commande pour copier un dossier
gsutil cp -r data/ gs://ihab_bucket_utopios/
# option -m pour faire de la parallélisation 
```
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

## Commande pour compute sur GCS

### Familles de machines

- **General purpose** (E2, N2, N2D)
    - Exemples: e2-medium (2 vCPU, 4GB), n2-standard-4 (4 vCPU, 16GB) 

- **Memory optimized** (M2, M3)
    - RAM importante
    - Spark
    - Exemple x4-megamem-1920 (1920 vCPU, 32TB RAM)

- **Accelerator Optimized** (A2, A4)
    - Avec GPU
    - ML Training, computer vision

**Type de disques**
- standard: pd-standard => HDD bon marché
- Balanced: SSD
- SSD
- Local SSD

```bash
gcloud compute instances create data-vm \
    --zone=europe-west1-b \
    --machine-type=e2-standard-2

# gcloud compute firewall-rules

```
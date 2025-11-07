## Etapes de la solution

### 1. Créer la VM

```bash
gcloud compute instances create data-processing-vm-ihab \
    --zone=europe-west1-b \
    --machine-type=e2-standard-2 \
    --tags=data-processing

gcloud compute instances list

```

### 2. Se connecter à la VM et installer les dépendances

```bash
gcloud compute ssh data-processing-vm-ihab --zone=europe-west1-b

# sur la vm
sudo apt update && sudo apt upgrade -y

sudo apt install -y python3-pip python3-venv

python3 -m venv ~/venv
source ~/venv/bin/activate

pip install pandas google-cloud-storage

```
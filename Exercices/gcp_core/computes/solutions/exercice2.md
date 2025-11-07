## Etapes:

### 1. création du script

### 2. Créer la machine

```bash
gcloud compute instances create exercice-2-ihab \
    --zone=europe-west1-b \
    --machine-type=e2-standard-2 \
    --tags=data-processing \
    --scopes=cloud-platform

gcloud compute ssh exercice-2-ihab 

# sur la vm
sudo apt update && sudo apt upgrade -y

sudo apt install -y python3-pip python3.11-venv

python3 -m venv ~/venv
source ~/venv/bin/activate

pip install pandas google-cloud-storage

```



### 3. Configurer le répertoire des logs
```bash
mkdir -p ~/logs
```

### 4. Copier le script

```bash
gcloud compute scp --recurse ../data/ ihababadi@exercice-2-ihab:~/
gcloud compute scp daily_report.py ihababadi@exercice-2-ihab:~/daily_report.py
gcloud compute ssh exercice-2-ihab 
python daily_report.py
```


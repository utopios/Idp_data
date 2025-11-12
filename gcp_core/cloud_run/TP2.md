# TP : Conversion Automatique CSV vers JSON avec Cloud Functions

## Contexte

Vous travaillez pour une entreprise qui reçoit quotidiennement des fichiers CSV de différentes sources. Vous devez automatiser la conversion de ces fichiers CSV en JSON pour faciliter leur intégration dans d'autres systèmes.

## Objectif

Créer une Cloud Function qui se déclenche automatiquement lorsqu'un fichier CSV est uploadé dans un bucket Cloud Storage, convertit ce fichier en JSON, et stocke le résultat dans un autre bucket.

## Architecture

```
Bucket "input"              Cloud Function              Bucket "output"
     |                            |                           |
     |  1. Upload CSV             |                           |
     |--------------------------->|                           |
     |                            |                           |
     |                       2. Trigger                       |
     |                            |                           |
     |                       3. Read CSV                      |
     |                            |                           |
     |                       4. Convert                       |
     |                            |                           |
     |                       5. Write JSON                    |
     |                            |-------------------------->|
```


## Prérequis

- Compte GCP actif
- gcloud CLI installé et configuré
- Connaissance de base de Python

## Partie 1 : Préparation

### Étape 1.1 : Activer les APIs nécessaires

```bash
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable storage.googleapis.com
```

### Étape 1.2 : Créer les buckets Cloud Storage

```bash
# Variables
export PROJECT_ID=$(gcloud config get-value project)
export REGION="europe-west1"

# Bucket pour les fichiers CSV d'entrée
gsutil mb -l $REGION gs://${PROJECT_ID}-csv-input

# Bucket pour les fichiers JSON de sortie
gsutil mb -l $REGION gs://${PROJECT_ID}-json-output

# Vérifier la création
gsutil ls
```

### Étape 1.3 : Créer la structure du projet

```bash
mkdir csv-to-json-function
cd csv-to-json-function
```

## Partie 2 : Code de la Cloud Function

### Étape 2.1 : Créer le fichier main.py

Créez le fichier `main.py` avec le contenu suivant :

```python
import functions_framework
from google.cloud import storage
import csv
import json
from datetime import datetime
import os

# Initialiser le client Storage
storage_client = storage.Client()

@functions_framework.cloud_event
def convert_csv_to_json(cloud_event):
    """
    Fonction déclenchée lors de l'upload d'un fichier dans Cloud Storage.
    Convertit un fichier CSV en JSON.
    
    Args:
        cloud_event: Événement Cloud Storage contenant les infos du fichier
    """
    # Extraire les informations de l'événement
    data = cloud_event.data
    
    bucket_name = data["bucket"]
    file_name = data["name"]
    
    print(f"Fichier détecté: {file_name} dans le bucket {bucket_name}")
    
    # Vérifier que c'est bien un fichier CSV
    if not file_name.endswith('.csv'):
        print(f"Le fichier {file_name} n'est pas un CSV, ignoré")
        return
    
    # Éviter de traiter les fichiers dans des sous-dossiers si nécessaire
    if file_name.startswith('processed/'):
        print(f"Fichier déjà traité, ignoré")
        return
    
    try:
        # Lire le fichier CSV depuis le bucket
        print(f"Lecture du fichier CSV...")
        source_bucket = storage_client.bucket(bucket_name)
        source_blob = source_bucket.blob(file_name)
        csv_content = source_blob.download_as_text()
        
        # Convertir CSV en JSON
        print(f"Conversion CSV -> JSON...")
        csv_lines = csv_content.strip().split('\n')
        csv_reader = csv.DictReader(csv_lines)
        
        # Convertir en liste de dictionnaires
        data_list = []
        for row in csv_reader:
            data_list.append(row)
        
        print(f"Nombre d'enregistrements convertis: {len(data_list)}")
        
        # Préparer le contenu JSON
        json_output = {
            "source_file": file_name,
            "conversion_date": datetime.now().isoformat(),
            "record_count": len(data_list),
            "data": data_list
        }
        
        json_content = json.dumps(json_output, indent=2, ensure_ascii=False)
        
        # Nom du fichier de sortie
        output_file_name = file_name.replace('.csv', '.json')
        
        # Écrire dans le bucket de sortie
        output_bucket_name = os.getenv('OUTPUT_BUCKET')
        if not output_bucket_name:
            print("ERREUR: Variable OUTPUT_BUCKET non définie")
            return
        
        print(f"Écriture dans le bucket de sortie: {output_bucket_name}")
        output_bucket = storage_client.bucket(output_bucket_name)
        output_blob = output_bucket.blob(output_file_name)
        output_blob.upload_from_string(json_content, content_type='application/json')
        
        print(f"✓ Conversion réussie: {output_file_name}")
        print(f"✓ Fichier disponible dans gs://{output_bucket_name}/{output_file_name}")
        
    except Exception as e:
        print(f"ERREUR lors de la conversion: {str(e)}")
        raise
```

### Étape 2.2 : Créer le fichier requirements.txt

Créez le fichier `requirements.txt` :

```txt
functions-framework==3.5.0
google-cloud-storage==2.13.0
```

### Étape 2.3 : Comprendre le code

Questions à répondre :

1. Quel est le nom du décorateur utilisé pour la Cloud Function ?
2. Pourquoi vérifie-t-on l'extension du fichier ?
3. À quoi sert la variable d'environnement OUTPUT_BUCKET ?
4. Que contient l'objet cloud_event.data ?

## Partie 3 : Déploiement de la Cloud Function (20 min)

### Étape 3.1 : Déployer la fonction

```bash
# Définir le bucket de sortie
export OUTPUT_BUCKET="${PROJECT_ID}-json-output"

# Déployer la Cloud Function (2ème génération)
gcloud functions deploy csv-to-json \
  --gen2 \
  --runtime python311 \
  --region $REGION \
  --source . \
  --entry-point convert_csv_to_json \
  --trigger-bucket ${PROJECT_ID}-csv-input \
  --set-env-vars OUTPUT_BUCKET=$OUTPUT_BUCKET \
  --memory 256Mi \
  --timeout 60s
```

### Étape 3.2 : Vérifier le déploiement

```bash
# Lister les fonctions
gcloud functions list --region $REGION

# Décrire la fonction
gcloud functions describe csv-to-json \
  --region $REGION \
  --gen2
```

## Partie 4 : Test de la Function 

### Étape 4.1 : Créer un fichier CSV de test

Créez le fichier `employes.csv` :

```csv
nom,prenom,age,departement,salaire
Dupont,Jean,35,IT,45000
Martin,Sophie,28,Marketing,38000
Bernard,Pierre,42,Finance,52000
Dubois,Marie,31,RH,41000
Laurent,Thomas,29,IT,43000
```

### Étape 4.2 : Uploader le fichier

```bash
# Upload dans le bucket d'entrée
gsutil cp employes.csv gs://${PROJECT_ID}-csv-input/

# Attendre quelques secondes pour le traitement
sleep 5

# Vérifier le fichier de sortie
gsutil ls gs://${PROJECT_ID}-json-output/
```

### Étape 4.3 : Télécharger et vérifier le résultat

```bash
# Télécharger le fichier JSON
gsutil cp gs://${PROJECT_ID}-json-output/employes.json .

# Afficher le contenu
cat employes.json | jq .
```

### Étape 4.4 : Vérifier les logs

```bash
# Voir les logs de la fonction
gcloud functions logs read csv-to-json \
  --region $REGION \
  --limit 50 \
  --gen2
```

## Partie 5 : Tests Supplémentaires 

### Test 1 : Fichier avec plus de données

Créez `ventes.csv` :

```csv
date,produit,quantite,prix_unitaire
2024-01-15,Laptop,5,899.99
2024-01-15,Souris,20,15.50
2024-01-16,Clavier,15,45.00
2024-01-16,Écran,8,299.99
2024-01-17,Webcam,12,79.90
```

```bash
gsutil cp ventes.csv gs://${PROJECT_ID}-csv-input/
sleep 3
gsutil cat gs://${PROJECT_ID}-json-output/ventes.json
```

### Test 2 : Fichier non-CSV (doit être ignoré)

```bash
echo "Test" > test.txt
gsutil cp test.txt gs://${PROJECT_ID}-csv-input/
gcloud functions logs read csv-to-json --region $REGION --limit 10 --gen2
```

Vous devriez voir dans les logs : "Le fichier test.txt n'est pas un CSV, ignoré"

## Partie 6 : Amélioration de la Function 

### Amélioration 1 : Ajouter la validation des données

Modifiez `main.py` pour ajouter une validation :

```python
def validate_csv_data(data_list):
    """Valide que les données CSV sont correctes"""
    if not data_list:
        raise ValueError("Le fichier CSV est vide")
    
    # Vérifier que toutes les lignes ont les mêmes colonnes
    first_keys = set(data_list[0].keys())
    for i, row in enumerate(data_list[1:], start=2):
        if set(row.keys()) != first_keys:
            raise ValueError(f"Ligne {i}: colonnes incohérentes")
    
    print(f"Validation OK: {len(data_list)} lignes, {len(first_keys)} colonnes")
    return True
```

Ajoutez l'appel à cette fonction dans la fonction principale :

```python
# Après la conversion CSV
data_list = list(csv_reader)
validate_csv_data(data_list)  # Ajouter cette ligne
```

### Amélioration 2 : Ajouter des statistiques

Ajoutez des statistiques dans le JSON de sortie :

```python
# Calculer des statistiques basiques
json_output = {
    "source_file": file_name,
    "conversion_date": datetime.now().isoformat(),
    "record_count": len(data_list),
    "columns": list(data_list[0].keys()) if data_list else [],
    "file_size_bytes": len(csv_content),
    "data": data_list
}
```

Redéployez la fonction :

```bash
gcloud functions deploy csv-to-json \
  --gen2 \
  --runtime python311 \
  --region $REGION \
  --source . \
  --entry-point convert_csv_to_json \
  --trigger-bucket ${PROJECT_ID}-csv-input \
  --set-env-vars OUTPUT_BUCKET=$OUTPUT_BUCKET
```

## Questions de Compréhension

1. Quelle est la différence entre Cloud Functions 1ère et 2ème génération ?
2. Pourquoi utilise-t-on `cloud_event.data` au lieu de paramètres classiques ?
3. Comment la fonction sait-elle quel fichier a été uploadé ?
4. Que se passe-t-il si on upload plusieurs fichiers en même temps ?
5. Pourquoi utilise-t-on une variable d'environnement pour le bucket de sortie ?

## Exercices Supplémentaires

### Exercice 1 : Gestion des erreurs

Modifiez la fonction pour :
- Créer un dossier "errors/" dans le bucket d'entrée
- Y déplacer les fichiers qui causent des erreurs
- Logger les erreurs de manière détaillée

### Exercice 2 : Support de formats additionnels

Ajoutez le support pour :
- Fichiers TSV (tab-separated values)
- Fichiers avec délimiteurs personnalisés
- Fichiers avec encoding différent (latin-1, etc.)

### Exercice 3 : Notification

Ajoutez une notification :
- Créer un topic Pub/Sub
- Publier un message après chaque conversion réussie
- Le message doit contenir le nom du fichier et le nombre d'enregistrements

## Nettoyage des Ressources

Pour éviter les frais, supprimez les ressources créées :

```bash
# Supprimer la Cloud Function
gcloud functions delete csv-to-json --region $REGION --gen2 --quiet

# Supprimer les buckets
gsutil -m rm -r gs://${PROJECT_ID}-csv-input
gsutil -m rm -r gs://${PROJECT_ID}-json-output

# Vérifier la suppression
gcloud functions list --region $REGION
gsutil ls
```

## Ajout des droits

```bash
export PROJECT_ID="projet-kube-c"
export BUCKET_NAME="ihab_bucket_utopios"
export REGION="europe-west1"

export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')

export EVENTARC_SA="service-${PROJECT_NUMBER}@gcp-sa-eventarc.iam.gserviceaccount.com"

gsutil iam ch serviceAccount:${EVENTARC_SA}:objectViewer gs://${BUCKET_NAME}
gsutil iam ch serviceAccount:${EVENTARC_SA}:legacyBucketReader gs://${BUCKET_NAME}


export GCS_SA="service-${PROJECT_NUMBER}@gs-project-accounts.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${GCS_SA}" \
  --role="roles/pubsub.publisher"

gsutil iam get gs://${BUCKET_NAME} | grep eventarc
```
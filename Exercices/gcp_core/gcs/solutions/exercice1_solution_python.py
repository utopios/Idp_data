#!/usr/bin/env python3

from google.cloud import storage
from pathlib import Path
import os
from datetime import datetime

BUCKET_NAME = "ihab_bucket_utopios"
PROJECT_ID = "projet-kube-c"
LOCATION = "europe-west1"

class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'


def print_step(step, total, message):
    print(f"\n{Colors.GREEN}[{step}/{total}] {message}{Colors.NC}")


def create_bucket(bucket_name, project_id, location):
    print_step(1, 4, "Création du bucket")

    storage_client = storage.Client(project=project_id)

    if storage_client.lookup_bucket(bucket_name):
        print(f"Le bucket {bucket_name} existe déjà")
        return storage_client.bucket(bucket_name)

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "STANDARD"
    new_bucket = storage_client.create_bucket(bucket, location=location)

    print(f"Bucket créé: {new_bucket.name}")
    print(f"  - Location: {new_bucket.location}")
    print(f"  - Storage class: {new_bucket.storage_class}")

    return new_bucket


def add_bucket_labels(bucket):
    print_step(2, 4, "Ajout de tags au bucket")

    labels = {
        'of': 'm2i',
        'type': 'data-lake',
        'department': 'analytics',
        'created': datetime.now().strftime('%Y%m%d')
    }

    bucket.labels = labels
    bucket.patch()

    print("Tags ajoutés au bucket:")
    for key, value in labels.items():
        print(f"  - {key}: {value}")


def create_folder_structure(bucket):
    print_step(3, 4, "Création de la structure de dossiers")

    folders = [
        "raw/ventes/2024/01/",
        "raw/ventes/2024/02/",
        "raw/logs/2024/01/",
        "processed/",
        "archive/"
    ]

    keep_content = f"Structure créée le {datetime.now().isoformat()}\n"

    for folder in folders:
        blob = bucket.blob(f"{folder}.keep")
        blob.upload_from_string(keep_content)
        print(f"  Créé: {folder}")

    print("Structure de dossiers créée")


def upload_files(bucket):
    print_step(4, 4, "Upload des fichiers")

    files_to_upload = [
        {
            'source': '../Exercice1/ventes_2024_01.csv',
            'destination': 'raw/ventes/2024/01/ventes_2024_01.csv'
        },
        {
            'source': '../Exercice1/ventes_2024_02.csv',
            'destination': 'raw/ventes/2024/02/ventes_2024_02.csv'
        },
        {
            'source': '../Exercice1logs/app_2024_01_15.log',
            'destination': 'raw/logs/2024/01/app_2024_01_15.log'
        },
        {
            'source': '../Exercice1logs/app_2024_01_16.log',
            'destination': 'raw/logs/2024/01/app_2024_01_16.log'
        }
    ]

    uploaded_count = 0
    total_size = 0

    for file_info in files_to_upload:
        source_path = Path(file_info['source'])

        if not source_path.exists():
            print(f"  Fichier non trouvé: {source_path}")
            continue

        blob = bucket.blob(file_info['destination'])
        blob.upload_from_filename(str(source_path))

        blob.metadata = {
            'uploaded_at': datetime.now().isoformat(),
            'original_name': source_path.name,
            'source': 'exercice_1'
        }
        blob.patch()

        file_size = source_path.stat().st_size
        total_size += file_size
        uploaded_count += 1

        print(f"  Uploadé: {source_path} -> gs://{bucket.name}/{file_info['destination']} ({file_size} bytes)")

    print(f"\n{uploaded_count} fichiers uploadés (Total: {total_size} bytes)")


def verify_structure(bucket):
    print(f"\n{Colors.BLUE}=== Vérification de la structure ==={Colors.NC}")

    blobs = bucket.list_blobs()

    print(f"\nContenu du bucket gs://{bucket.name}:")
    for blob in blobs:
        print(f"  - {blob.name} ({blob.size} bytes)")


def display_bucket_info(bucket):
    print(f"\n{Colors.BLUE}=== Informations du bucket ==={Colors.NC}")

    bucket.reload()

    print(f"Nom: {bucket.name}")
    print(f"Location: {bucket.location}")
    print(f"Storage Class: {bucket.storage_class}")
    print(f"Created: {bucket.time_created}")

    if bucket.labels:
        print("\nLabels:")
        for key, value in bucket.labels.items():
            print(f"  - {key}: {value}")


def main():
    print(f"{Colors.BLUE}=== Exercice 1: Organisation du Data Lake ==={Colors.NC}")
    print(f"Bucket: {BUCKET_NAME}")
    print(f"Project: {PROJECT_ID}")

    try:
        bucket = create_bucket(BUCKET_NAME, PROJECT_ID, LOCATION)
        add_bucket_labels(bucket)
        create_folder_structure(bucket)
        upload_files(bucket)
        verify_structure(bucket)
        display_bucket_info(bucket)

        print(f"\n{Colors.GREEN}Exercice 1 terminé avec succès!{Colors.NC}")

        print(f"\n{Colors.BLUE}Commandes utiles:{Colors.NC}")
        print(f"  - Lister le contenu: gsutil ls -r gs://{BUCKET_NAME}")
        print(f"  - Supprimer le bucket: gsutil rm -r gs://{BUCKET_NAME}")
        print(f"  - Console Web: https://console.cloud.google.com/storage/browser/{BUCKET_NAME}")

    except Exception as e:
        print(f"\n{Colors.YELLOW}Erreur: {e}{Colors.NC}")
        raise


if __name__ == "__main__":
    required_files = [
        "data/ventes_2024_01.csv",
        "data/ventes_2024_02.csv",
        "logs/app_2024_01_15.log",
        "logs/app_2024_01_16.log"
    ]

    missing_files = [f for f in required_files if not Path(f).exists()]

    if missing_files:
        print(f"{Colors.YELLOW}Fichiers manquants:{Colors.NC}")
        for f in missing_files:
            print(f"  - {f}")
        print("\nAssurez-vous d'exécuter le script depuis le dossier Exercices/gcp_core/gcs/solutions/")

    main()

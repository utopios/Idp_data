from google.cloud import storage
from pathlib import Path
import os
from datetime import datetime
import pandas as pd
from exercie_tools import Colors

BUCKET_NAME = "ihab_bucket_utopios"
PROJECT_ID = "projet-kube-c"
LOCATION = "europe-west1"
CSV_LOCAL_PATH = "transactions/transactions_1000.csv"


def csv_to_parquet(csv_path, parquet_path):
    print(f"{Colors.BLUE}Conversion du fichier CSV en Parquet...{Colors.NC}")
    if not Path(csv_path).is_file():
        print(f"{Colors.YELLOW}Le fichier CSV spécifié n'existe pas: {csv_path}{Colors.NC}")
        return
    
    df = pd.read_csv(csv_path)
    df.to_parquet(parquet_path, index=False)
    print(f"Fichier Parquet créé: {parquet_path}")

def upload_file_to_gcs(bucket_name, source_file_path, destination_blob_name):
    print(f"{Colors.BLUE}Téléversement du fichier vers GCS...{Colors.NC}")
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_path)
    print(f"Fichier {source_file_path} téléversé vers gs://{bucket_name}/{destination_blob_name}")

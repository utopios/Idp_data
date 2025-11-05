from google.cloud import storage
from pathlib import Path
import os
from datetime import datetime
import pandas as pd
from exercie_tools import Colors
import sys

BUCKET_NAME = "ihab_bucket_utopios"
PROJECT_ID = "projet-kube-c"
LOCATION = "europe-west1"
CSV_LOCAL_PATH = "transactions/transactions_1000.csv"


class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'


def format_bytes(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def csv_to_parquet_local(csv_path):
    print(f"{Colors.BLUE}=== Exercice 3: Conversion CSV vers Parquet ==={Colors.NC}\n")

    print(f"{Colors.GREEN}[1/4] Lecture du fichier CSV local{Colors.NC}")

    if not Path(csv_path).exists():
        print(f"{Colors.YELLOW}Fichier non trouvé: {csv_path}{Colors.NC}")
        print("Assurez-vous d'exécuter le script depuis le dossier exercices-gcp/")
        return None

    csv_size = Path(csv_path).stat().st_size
    print(f"Fichier: {csv_path}")
    print(f"Taille CSV: {csv_size:,} bytes ({format_bytes(csv_size)})")

    try:
        df = pd.read_csv(csv_path)
        print(f"Lignes: {len(df):,}")
        print(f"Colonnes: {len(df.columns)}")
        print(f"\nAperçu des données:")
        print(df.head())
        print(f"\nTypes de colonnes:")
        print(df.dtypes)

    except Exception as e:
        print(f"{Colors.YELLOW}Erreur lecture CSV: {e}{Colors.NC}")
        return None

    print(f"\n{Colors.GREEN}[2/4] Conversion CSV vers Parquet{Colors.NC}")

    parquet_path = csv_path.replace('.csv', '.parquet')

    try:
        df.to_parquet(
            parquet_path,
            compression='snappy',
            engine='pyarrow',
            index=False
        )
        print(f"Conversion réussie!")
        print(f"Fichier Parquet: {parquet_path}")

    except Exception as e:
        print(f"{Colors.YELLOW}Erreur conversion: {e}{Colors.NC}")
        return None

    parquet_size = Path(parquet_path).stat().st_size
    print(f"Taille Parquet: {parquet_size:,} bytes ({format_bytes(parquet_size)})")

    return {
        'csv_path': csv_path,
        'parquet_path': parquet_path,
        'csv_size': csv_size,
        'parquet_size': parquet_size,
        'df': df
    }


def upload_to_gcs(data, bucket_name, project_id):
    print(f"\n{Colors.GREEN}[3/4] Upload vers GCS{Colors.NC}")

    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)

    csv_blob_name = "transactions/transactions_1000.csv"
    parquet_blob_name = "transactions/transactions_1000.parquet"

    print(f"Upload du CSV...")
    csv_blob = bucket.blob(csv_blob_name)
    csv_blob.metadata = {
        'format': 'csv',
        'size': str(data['csv_size']),
        'rows': str(len(data['df'])),
        'columns': str(len(data['df'].columns))
    }
    csv_blob.upload_from_filename(data['csv_path'])
    print(f"  -> gs://{bucket_name}/{csv_blob_name}")

    print(f"Upload du Parquet...")
    parquet_blob = bucket.blob(parquet_blob_name)
    parquet_blob.metadata = {
        'format': 'parquet',
        'compression': 'snappy',
        'size': str(data['parquet_size']),
        'rows': str(len(data['df'])),
        'columns': str(len(data['df'].columns)),
        'original_csv_size': str(data['csv_size'])
    }
    parquet_blob.upload_from_filename(data['parquet_path'])
    print(f"  -> gs://{bucket_name}/{parquet_blob_name}")

    return csv_blob_name, parquet_blob_name


def compare_sizes(data):
    print(f"\n{Colors.GREEN}[4/4] Comparaison des tailles{Colors.NC}")

    csv_size = data['csv_size']
    parquet_size = data['parquet_size']

    saved = csv_size - parquet_size
    ratio = (1 - parquet_size / csv_size) * 100

    print(f"\nFormat CSV:")
    print(f"  - Taille: {csv_size:,} bytes ({format_bytes(csv_size)})")

    print(f"\nFormat Parquet:")
    print(f"  - Taille: {parquet_size:,} bytes ({format_bytes(parquet_size)})")
    print(f"  - Compression: snappy")

    print(f"\nGain:")
    print(f"  - Économie: {saved:,} bytes ({format_bytes(saved)})")
    print(f"  - Ratio de compression: {ratio:.2f}%")

    return saved, ratio


def csv_to_parquet_from_gcs(bucket_name, project_id, gcs_csv_path):
    print(f"{Colors.BLUE}=== Conversion CSV vers Parquet (depuis GCS) ==={Colors.NC}\n")

    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)

    print(f"{Colors.GREEN}[1/3] Téléchargement du CSV depuis GCS{Colors.NC}")
    print(f"Source: gs://{bucket_name}/{gcs_csv_path}")

    local_csv = "temp_download.csv"

    try:
        blob = bucket.blob(gcs_csv_path)
        blob.download_to_filename(local_csv)
        csv_size = Path(local_csv).stat().st_size
        print(f"Téléchargé: {csv_size:,} bytes ({format_bytes(csv_size)})")

    except Exception as e:
        print(f"{Colors.YELLOW}Erreur téléchargement: {e}{Colors.NC}")
        return

    print(f"\n{Colors.GREEN}[2/3] Conversion et upload{Colors.NC}")

    try:
        df = pd.read_csv(local_csv)
        print(f"Lignes: {len(df):,}, Colonnes: {len(df.columns)}")

        local_parquet = "temp_download.parquet"
        df.to_parquet(local_parquet, compression='snappy', engine='pyarrow', index=False)

        parquet_size = Path(local_parquet).stat().st_size

        parquet_blob_name = gcs_csv_path.replace('.csv', '.parquet')
        parquet_blob = bucket.blob(parquet_blob_name)
        parquet_blob.upload_from_filename(local_parquet)

        print(f"Uploadé: gs://{bucket_name}/{parquet_blob_name}")

        os.remove(local_csv)
        os.remove(local_parquet)

    except Exception as e:
        print(f"{Colors.YELLOW}Erreur: {e}{Colors.NC}")
        return

    print(f"\n{Colors.GREEN}[3/3] Comparaison{Colors.NC}")
    saved = csv_size - parquet_size
    ratio = (1 - parquet_size / csv_size) * 100

    print(f"CSV: {csv_size:,} bytes ({format_bytes(csv_size)})")
    print(f"Parquet: {parquet_size:,} bytes ({format_bytes(parquet_size)})")
    print(f"Économie: {saved:,} bytes ({ratio:.2f}%)")


if __name__ == "__main__":
    if not BUCKET_NAME or not PROJECT_ID:
        print(f"{Colors.YELLOW}Veuillez configurer BUCKET_NAME et PROJECT_ID{Colors.NC}")
        sys.exit(1)

    data = csv_to_parquet_local(CSV_LOCAL_PATH)

    if data:
        csv_blob, parquet_blob = upload_to_gcs(data, BUCKET_NAME, PROJECT_ID)
        saved, ratio = compare_sizes(data)

        print(f"\n{Colors.BLUE}=== Résumé ==={Colors.NC}")
        print(f"\nFichiers locaux:")
        print(f"  - CSV: {data['csv_path']}")
        print(f"  - Parquet: {data['parquet_path']}")

        print(f"\nFichiers GCS:")
        print(f"  - CSV: gs://{BUCKET_NAME}/{csv_blob}")
        print(f"  - Parquet: gs://{BUCKET_NAME}/{parquet_blob}")

        print(f"\nPerformance:")
        print(f"  - Économie d'espace: {ratio:.2f}%")
        print(f"  - Format recommandé: Parquet pour le stockage et l'analyse")

        print(f"\n{Colors.GREEN}Conversion terminée avec succès!{Colors.NC}")

        print(f"\n{Colors.BLUE}Commandes utiles:{Colors.NC}")
        print(f"  - Lister: gsutil ls -lh gs://{BUCKET_NAME}/transactions/")
        print(f"  - Télécharger: gsutil cp gs://{BUCKET_NAME}/{parquet_blob} .")

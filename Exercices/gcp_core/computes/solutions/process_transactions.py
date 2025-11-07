"""
Script de traitement des transactions depuis GCS
Télécharge un fichier CSV, calcule les ventes par catégorie et sauvegarde le résultat
"""

from google.cloud import storage
import pandas as pd
import sys
from datetime import datetime

# Configuration
BUCKET_NAME = 'ihab_bucket_utopios'  
INPUT_FILE = 'transactions_500.csv'
OUTPUT_FILE = 'processed/summary.csv'

def download_from_gcs(bucket_name, blob_name, local_filename):
    """Télécharge un fichier depuis GCS"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Téléchargement de {blob_name}...")

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.download_to_filename(local_filename)
    blob.reload()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Fichier téléchargé: {local_filename}")

    return blob.size

def process_transactions(input_file):
    """Traite les transactions et calcule les statistiques par catégorie"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Traitement des données...")

    # Charger les données
    df = pd.read_csv(input_file)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Nombre de transactions: {len(df)}")

    # Calculer les statistiques par catégorie
    summary = df.groupby('categorie').agg({
        'montant': ['sum', 'mean', 'count']
    }).round(2)

    # Renommer les colonnes pour plus de clarté
    summary.columns = ['total_ventes', 'montant_moyen', 'nombre_transactions']

    # Trier par total de ventes décroissant
    summary = summary.sort_values('total_ventes', ascending=False)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Traitement terminé")
    print("\nRésultats:")
    print(summary)

    return summary

def upload_to_gcs(bucket_name, blob_name, local_filename):
    """Upload un fichier vers GCS"""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Upload vers {blob_name}...")

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_filename(local_filename)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Fichier uploadé avec succès")

    return blob.size

def main():
    """Fonction principale"""
    print("="*60)
    print("Script de traitement des transactions")
    print("="*60)

    try:
        # Étape 1: Télécharger le fichier depuis GCS
        local_input = '/tmp/transactions.csv'
        download_size = download_from_gcs(BUCKET_NAME, INPUT_FILE, local_input)
        print(f"Taille du fichier: {download_size / 1024:.2f} KB")

        # Étape 2: Traiter les données
        summary = process_transactions(local_input)

        # Étape 3: Sauvegarder le résultat localement
        local_output = '/tmp/summary.csv'
        summary.to_csv(local_output)
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Résultat sauvegardé: {local_output}")

        # Étape 4: Upload vers GCS
        upload_size = upload_to_gcs(BUCKET_NAME, OUTPUT_FILE, local_output)
        print(f"Taille du résultat: {upload_size / 1024:.2f} KB")

        print("\n" + "="*60)
        print("✓ Traitement terminé avec succès!")
        print("="*60)

        return 0

    except Exception as e:
        print(f"\n✗ Erreur lors du traitement: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
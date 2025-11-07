"""
Script de traitement quotidien des ventes
S'exécute automatiquement chaque jour à 2h du matin via cron
"""

from google.cloud import storage
import pandas as pd
from datetime import datetime, timedelta
import sys
import logging

# Configuration du logging
log_file = '/home/ihababadi/logs/daily_report.log' # A modifier selon votre configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Configuration
BUCKET_NAME = 'ihab_bucket_utopios' 
VENTES_FILES = [
    'data/ventes_2024_01.csv',
    'data/ventes_2024_02.csv'
]

def download_file(bucket_name, blob_name, local_filename):
    """Télécharge un fichier depuis GCS"""
    try:
        logging.info(f"Téléchargement de {blob_name}...")
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.download_to_filename(local_filename)
        logging.info(f"✓ Fichier téléchargé: {local_filename}")
        return True
    except Exception as e:
        logging.error(f"✗ Erreur lors du téléchargement: {e}")
        return False

def process_sales_data(files):
    """Traite les données de ventes"""
    try:
        logging.info("Traitement des données de ventes...")

        all_data = []
        for file in files:
            df = pd.read_csv(file)
            all_data.append(df)

        # Combiner toutes les données
        df_combined = pd.concat(all_data, ignore_index=True)

        # Convertir la date
        df_combined['date'] = pd.to_datetime(df_combined['date'])

        # Calculer les statistiques
        stats = {
            'total_ventes': len(df_combined),
            'revenu_total': (df_combined['quantite'] * df_combined['prix']).sum(),
            'quantite_totale': df_combined['quantite'].sum()
        }

        # Ventes par produit
        ventes_par_produit = df_combined.groupby('produit').agg({
            'quantite': 'sum',
            'prix': 'mean'
        }).round(2)

        # Ventes par région
        ventes_par_region = df_combined.groupby('region').agg({
            'quantite': 'sum'
        })

        # Ventes par jour
        ventes_par_jour = df_combined.groupby(df_combined['date'].dt.date).agg({
            'quantite': 'sum',
            'prix': lambda x: (df_combined.loc[x.index, 'quantite'] * df_combined.loc[x.index, 'prix']).sum()
        })

        logging.info(f"Total de ventes: {stats['total_ventes']}")
        logging.info(f"Revenu total: {stats['revenu_total']:.2f} EUR")
        logging.info(f"Quantité totale: {stats['quantite_totale']}")

        return {
            'stats': stats,
            'par_produit': ventes_par_produit,
            'par_region': ventes_par_region,
            'par_jour': ventes_par_jour
        }

    except Exception as e:
        logging.error(f"✗ Erreur lors du traitement: {e}")
        return None

def generate_report(results):
    """Génère un rapport en format texte"""
    try:
        report_file = f"/tmp/rapport_quotidien_{datetime.now().strftime('%Y%m%d')}.txt"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write(f"RAPPORT QUOTIDIEN DES VENTES - {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            f.write("=" * 70 + "\n\n")

            # Statistiques globales
            f.write("STATISTIQUES GLOBALES\n")
            f.write("-" * 70 + "\n")
            f.write(f"Nombre total de ventes: {results['stats']['total_ventes']}\n")
            f.write(f"Revenu total: {results['stats']['revenu_total']:.2f} EUR\n")
            f.write(f"Quantité totale vendue: {results['stats']['quantite_totale']}\n\n")

            # Ventes par produit
            f.write("VENTES PAR PRODUIT\n")
            f.write("-" * 70 + "\n")
            f.write(results['par_produit'].to_string())
            f.write("\n\n")

            # Ventes par région
            f.write("VENTES PAR RÉGION\n")
            f.write("-" * 70 + "\n")
            f.write(results['par_region'].to_string())
            f.write("\n\n")

            # Ventes par jour
            f.write("VENTES PAR JOUR\n")
            f.write("-" * 70 + "\n")
            f.write(results['par_jour'].to_string())
            f.write("\n\n")

            f.write("=" * 70 + "\n")
            f.write("Fin du rapport\n")
            f.write("=" * 70 + "\n")

        logging.info(f"Rapport généré: {report_file}")
        return report_file

    except Exception as e:
        logging.error(f"Erreur lors de la génération du rapport: {e}")
        return None

def upload_report(bucket_name, local_file):
    """Upload le rapport vers GCS"""
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)

        blob_name = f"reports/daily_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(local_file)

        logging.info(f"Rapport uploadé: {blob_name}")
        return True

    except Exception as e:
        logging.error(f"Erreur lors de l'upload: {e}")
        return False

def main():
    """Fonction principale"""
    logging.info("=" * 70)
    logging.info("Démarrage du traitement quotidien")
    logging.info("=" * 70)

    try:
        # Télécharger les fichiers de ventes
        local_files = []
        for i, vente_file in enumerate(VENTES_FILES):
            local_file = f"/tmp/ventes_{i}.csv"
            if download_file(BUCKET_NAME, vente_file, local_file):
                local_files.append(local_file)
            else:
                logging.error(f"Échec du téléchargement de {vente_file}")
                return 1

        # Traiter les données
        results = process_sales_data(local_files)
        if not results:
            logging.error("Échec du traitement des données")
            return 1

        # Générer le rapport
        report_file = generate_report(results)
        if not report_file:
            logging.error("Échec de la génération du rapport")
            return 1

        # Upload vers GCS
        if not upload_report(BUCKET_NAME, report_file):
            logging.error("Échec de l'upload du rapport")
            return 1

        logging.info("=" * 70)
        logging.info("Traitement quotidien terminé avec succès")
        logging.info("=" * 70)

        return 0

    except Exception as e:
        logging.error(f"✗ Erreur fatale: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
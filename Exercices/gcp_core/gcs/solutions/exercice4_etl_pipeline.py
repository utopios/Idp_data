"""
Pipeline ETL Simple - Exercice 4
Extrait, Transforme et Charge des données CSV depuis/vers Google Cloud Storage
"""

from google.cloud import storage
import pandas as pd
import io
from datetime import datetime
import sys


class ETLPipeline:
    """Pipeline ETL pour nettoyer des données de ventes"""

    def __init__(self, bucket_name):
        """
        Initialise le pipeline ETL

        Args:
            bucket_name: Nom du bucket GCS
        """
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)

    def extract(self, source_blob_name):
        """
        EXTRACT: Télécharge un fichier CSV depuis Google Cloud Storage

        Args:
            source_blob_name: Nom du fichier dans GCS (ex: 'data/ventes_invalides.csv')

        Returns:
            DataFrame pandas avec les données brutes
        """
        print(f"EXTRACT: Téléchargement de {source_blob_name} depuis GCS...")

        blob = self.bucket.blob(source_blob_name)

        # Télécharger le contenu du blob
        content = blob.download_as_bytes()

        # Convertir en DataFrame
        df = pd.read_csv(io.BytesIO(content))

        print(f"   {len(df)} lignes extraites")
        print(f"   Colonnes: {list(df.columns)}")

        return df

    def transform(self, df):
        """
        TRANSFORM: Nettoie les données en supprimant les lignes avec valeurs manquantes

        Args:
            df: DataFrame pandas avec les données brutes

        Returns:
            DataFrame pandas nettoyé
        """
        print(f"\nTRANSFORM: Nettoyage des données...")

        initial_rows = len(df)
        print(f"   • Lignes initiales: {initial_rows}")

        # Afficher les valeurs manquantes par colonne
        missing_per_column = df.isnull().sum()
        if missing_per_column.any():
            print("\n   Valeurs manquantes détectées:")
            for col, count in missing_per_column[missing_per_column > 0].items():
                print(f"     - {col}: {count} valeurs manquantes")

        # Supprimer les lignes avec des valeurs manquantes
        df_clean = df.dropna()

        final_rows = len(df_clean)
        rows_removed = initial_rows - final_rows

        print(f"\n   Lignes supprimées: {rows_removed}")
        print(f"   Lignes conservées: {final_rows}")
        print(f"   Taux de conservation: {(final_rows/initial_rows)*100:.1f}%")

        return df_clean

    def load(self, df, destination_blob_name):
        """
        LOAD: Upload le DataFrame nettoyé vers Google Cloud Storage

        Args:
            df: DataFrame pandas nettoyé
            destination_blob_name: Nom du fichier de destination dans GCS
        """
        print(f"\nLOAD: Upload vers {destination_blob_name} dans GCS...")

        # Convertir le DataFrame en CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        # Upload vers GCS
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')
        # Ajouter des métadonnées
        blob.metadata = {'uploaded_at': datetime.utcnow().isoformat() + 'Z'}
        blob.patch()
        print(f"   Fichier uploadé avec succès!")
        print(f"   URI: gs://{self.bucket_name}/{destination_blob_name}")

    def run(self, source_blob_name, destination_blob_name=None):
        """
        Exécute le pipeline ETL complet

        Args:
            source_blob_name: Fichier source dans GCS
            destination_blob_name: Fichier de destination dans GCS (optionnel)
        """
        print("=" * 70)
        print("DÉMARRAGE DU PIPELINE ETL")
        print("=" * 70)

        # Générer le nom de destination si non fourni
        if destination_blob_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = source_blob_name.replace('.csv', '')
            destination_blob_name = f"{base_name}_cleaned_{timestamp}.csv"

        try:
            # EXTRACT
            df_raw = self.extract(source_blob_name)

            # TRANSFORM
            df_clean = self.transform(df_raw)

            # LOAD
            self.load(df_clean, destination_blob_name)

            print("\n" + "=" * 70)
            print("PIPELINE ETL TERMINÉ AVEC SUCCÈS!")
            print("=" * 70)

            return df_clean

        except Exception as e:
            print(f"\nERREUR: {str(e)}")
            raise


def main():
    """Fonction principale"""

    # Configuration
    BUCKET_NAME = "ihab_bucket_utopios"  # À modifier selon votre bucket
    SOURCE_FILE = "../Exercice1/ventes_invalides.csv"
    DESTINATION_FILE = "../Exercice1/ventes_cleaned.csv"  # Optionnel

    # Vérifier les arguments de ligne de commande
    if len(sys.argv) > 1:
        BUCKET_NAME = sys.argv[1]
    if len(sys.argv) > 2:
        SOURCE_FILE = sys.argv[2]
    if len(sys.argv) > 3:
        DESTINATION_FILE = sys.argv[3]

    # Créer et exécuter le pipeline
    pipeline = ETLPipeline(BUCKET_NAME)
    df_result = pipeline.run(SOURCE_FILE, DESTINATION_FILE)

    # Afficher un aperçu des données nettoyées
    print("\nAperçu des données nettoyées:")
    print(df_result.to_string(index=False))


if __name__ == "__main__":
    main()

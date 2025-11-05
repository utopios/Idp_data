from google.cloud import storage
from pathlib import Path
import os
import zipfile
from datetime import datetime
from tqdm import tqdm
import logging

from exercie_tools import Colors

BUCKET_NAME = "ihab_bucket_utopios"
PROJECT_ID = "projet-kube-c"
LOCATION = "europe-west1"
LOCAL_DIR_TO_ZIP = "../Exercice1"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("backup.log")
    ]
    )
 
logger = logging.getLogger(__name__)

def create_zip_backup(localdir, zip_filename):
    
    files = [f for f in Path(localdir).rglob('**/*') if f.is_file()]

    if not files:
        logger.warning(f"Aucun fichier trouvé dans le répertoire {localdir} pour la sauvegarde.")
        return None, 0, 0

    total_original_size = 0

    logger.info(f"Création de l'archive ZIP: {zip_filename}")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for file in tqdm(files, desc="Ajout des fichiers à l'archive ZIP", unit="file"):
            try:
                zipf.write(file, file.relative_to(localdir))
                total_original_size += file.stat().st_size
            except Exception as e:
                logger.error(f"Erreur lors de l'ajout du fichier {file} à l'archive ZIP: {e}")
    zip_size = Path(zip_filename).stat().st_size
    logger.info("Archive ZIP créée avec succès.")
    return len(files), total_original_size, zip_size


def backup_to_gcs(bucket_name, localdir, project_id):
    print(f"{Colors.BLUE}Démarrage de la sauvegarde vers GCS...{Colors.NC}")
    today_str = datetime.now().strftime('%Y-%m-%d')
    backup_prefix = f"backups/{today_str}/"
    zip_filename = f"backup_{today_str}.zip"

    print(f"Date : {today_str}")
    print(f"Dossier local à sauvegarder : {localdir}")
    print(f"Destination GCS : gs://{bucket_name}/{backup_prefix}{zip_filename}")

    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)

    local_path = Path(localdir)
    if not local_path.exists():
        logger.error(f"Le répertoire local {localdir} n'existe pas. Abandon de la sauvegarde.")
        return
    
    print("Création de l'archive ZIP...")
    num_files, total_original_size, zip_size = create_zip_backup(localdir, zip_filename)
    if num_files == 0:
        print(f"{Colors.YELLOW}Aucun fichier à sauvegarder. Abandon de la sauvegarde.{Colors.NC}")
        return
    print(f"Nombre de fichiers archivés : {num_files}")
    print(f"Taille totale originale : {total_original_size} bytes")
    print(f"Taille de l'archive ZIP : {zip_size} bytes")
    print("Upload de l'archive ZIP vers GCS...")
    blob = bucket.blob(f"{backup_prefix}{zip_filename}")
    try:
        blob.upload_from_filename(zip_filename)
        blob.metadata = {
            'backup_date': today_str,
            'original_size_bytes': str(total_original_size),
            'zip_size_bytes': str(zip_size),
            'num_files': str(num_files)
        }
        blob.patch()
        print(f"{Colors.GREEN}Sauvegarde réussie vers gs://{bucket_name}/{backup_prefix}{zip_filename}{Colors.NC}")
        logger.info(f"Sauvegarde réussie: {num_files} fichiers ({total_original_size} bytes) archivés dans {zip_size} bytes.")
    except Exception as e:
        logger.error(f"Erreur lors de l'upload vers GCS: {e}")
        print(f"{Colors.RED}Erreur lors de l'upload vers GCS.{Colors.NC}")

if __name__ == "__main__":
    backup_to_gcs(BUCKET_NAME, LOCAL_DIR_TO_ZIP, PROJECT_ID)
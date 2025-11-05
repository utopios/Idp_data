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




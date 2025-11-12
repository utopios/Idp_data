from google.cloud import storage
from datetime import datetime
import os
from io import StringIO

class WeatherStorageHandler:
    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
    
    def upload_file(self, file_content, station_id, original_filename):
        """
        Upload le fichier CSV dans Cloud Storage avec organisation par date
        
        Structure: raw/YYYY/MM/filename_timestamp.csv
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        year = datetime.now().year
        month = datetime.now().month
        
        filename = f"weather_{timestamp}.csv"
        blob_path = f"raw/{year}/{month:02d}/{filename}"
        
        blob = self.bucket.blob(blob_path)
        blob.upload_from_string(file_content, content_type='text/csv')
        
        # Ajouter des métadonnées
        blob.metadata = {
            'station_id': station_id,
            'original_filename': original_filename,
            'upload_timestamp': datetime.now().isoformat()
        }
        blob.patch()
        
        return blob_path, filename
    
    def list_files(self, prefix='raw/', station_id=None, year=None):
        """Liste les fichiers avec filtres optionnels"""
        if year:
            prefix = f"raw/{year}/"
        
        blobs = self.bucket.list_blobs(prefix=prefix)
        
        files = []
        for blob in blobs:
            if station_id and blob.metadata.get('station_id') != station_id:
                continue
            
            files.append({
                'name': blob.name,
                'size_bytes': blob.size,
                'upload_date': blob.time_created.isoformat(),
                'station_id': blob.metadata.get('station_id', 'unknown')
            })
        
        return files
    
    def download_file(self, blob_path):
        """Télécharge un fichier depuis Cloud Storage"""
        blob = self.bucket.blob(blob_path)
        return blob.download_as_text()
    
    def get_all_data_for_station(self, station_id):
        """
        Récupère et combine toutes les données d'une station
        Retourne un DataFrame pandas
        """
        import pandas as pd
        
        files = self.list_files(station_id=station_id)
        dfs = []
        
        for file_info in files:
            content = self.download_file(file_info['name'])
            df = pd.read_csv(StringIO(content))
            dfs.append(df)
        
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        return pd.DataFrame()
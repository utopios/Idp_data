import pandas as pd
from werkzeug.datastructures import FileStorage
from io import StringIO
class DataValidator:
    REQUIRED_COLUMNS = ['date', 'temperature', 'humidity', 'pressure', 
                        'wind_speed', 'precipitation', 'station_id']
    
    @staticmethod
    def validate_csv_file(file: FileStorage):
        """Valide le format du fichier CSV"""
        if not file.filename.endswith('.csv'):
            return False, "Le fichier doit être au format CSV"
        
        try:
            content = file.read()
            file.seek(0)  # Reset pour pouvoir relire
            
            df = pd.read_csv(StringIO(content.decode('utf-8')))
            
            # Vérifier les colonnes requises
            missing_cols = set(DataValidator.REQUIRED_COLUMNS) - set(df.columns)
            if missing_cols:
                return False, f"Colonnes manquantes: {missing_cols}"
            
            # Vérifier les types de données
            df['date'] = pd.to_datetime(df['date'])
            
            numeric_cols = ['temperature', 'humidity', 'pressure', 
                           'wind_speed', 'precipitation']
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col])
            
            # Vérifier les valeurs
            if df['humidity'].min() < 0 or df['humidity'].max() > 100:
                return False, "L'humidité doit être entre 0 et 100"
            
            if df['temperature'].min() < -50 or df['temperature'].max() > 60:
                return False, "Température hors limites réalistes"
            
            return True, df
            
        except Exception as e:
            return False, f"Erreur de validation: {str(e)}"
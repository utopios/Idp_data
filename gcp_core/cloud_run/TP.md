# TP Data : API d'Analyse de Données Météorologiques

## Contexte

Vous êtes data engineer dans une entreprise d'analyse climatique. Vous devez créer une API REST qui permet d'uploader des fichiers CSV contenant des données météorologiques, de les stocker, de les analyser et de fournir des statistiques via des endpoints.

## Objectifs

Créer une application Cloud Run qui :
1. Reçoit des fichiers CSV de données météorologiques
2. Stocke les fichiers bruts dans Cloud Storage
3. Analyse les données avec pandas
4. Retourne des statistiques et visualisations
5. Permet de requêter les données historiques

## Architecture

```
Client → Cloud Run API → Cloud Storage
                ↓
         Analyse pandas
                ↓
         Résultats JSON
```

## Spécifications Techniques

### Format des Données d'Entrée

Fichier CSV avec les colonnes suivantes :
- date : format YYYY-MM-DD
- temperature : température en Celsius
- humidity : humidité en pourcentage
- pressure : pression atmosphérique en hPa
- wind_speed : vitesse du vent en km/h
- precipitation : précipitations en mm
- station_id : identifiant de la station météo

Exemple :
```csv
date,temperature,humidity,pressure,wind_speed,precipitation,station_id
2024-01-01,15.2,65,1013.2,12.5,0.0,STATION_01
2024-01-02,16.8,70,1012.8,15.2,2.3,STATION_01
```

### Endpoints à Implémenter

#### 1. POST /api/upload
Upload un fichier CSV de données météorologiques

**Request:**
- Content-Type: multipart/form-data
- Body: fichier CSV + station_id (optionnel)

**Response:**
```json
{
  "status": "success",
  "file_name": "weather_20240101_120000.csv",
  "records_count": 365,
  "storage_path": "raw/2024/01/weather_20240101_120000.csv",
  "upload_timestamp": "2024-01-01T12:00:00Z"
}
```

#### 2. GET /api/statistics/{station_id}
Récupère les statistiques globales pour une station

**Query Parameters:**
- start_date : date de début (optionnel)
- end_date : date de fin (optionnel)

**Response:**
```json
{
  "station_id": "STATION_01",
  "period": {
    "start": "2024-01-01",
    "end": "2024-12-31"
  },
  "statistics": {
    "temperature": {
      "mean": 18.5,
      "min": -2.3,
      "max": 35.7,
      "std": 8.2
    },
    "humidity": {
      "mean": 68.4,
      "min": 35,
      "max": 95,
      "std": 12.1
    },
    "total_precipitation": 847.3,
    "records_count": 365
  }
}
```

#### 3. GET /api/monthly-summary/{station_id}/{year}
Résumé mensuel des données

**Response:**
```json
{
  "station_id": "STATION_01",
  "year": 2024,
  "monthly_data": [
    {
      "month": 1,
      "avg_temperature": 12.3,
      "total_precipitation": 45.2,
      "days_with_rain": 12
    },
    ...
  ]
}
```

#### 4. GET /api/anomalies/{station_id}
Détecte les anomalies dans les données

**Query Parameters:**
- threshold : écart-type pour détecter les anomalies (défaut: 3)

**Response:**
```json
{
  "station_id": "STATION_01",
  "anomalies": [
    {
      "date": "2024-06-15",
      "variable": "temperature",
      "value": 42.5,
      "mean": 25.3,
      "std": 4.2,
      "z_score": 4.1,
      "severity": "high"
    }
  ],
  "total_anomalies": 3
}
```

#### 5. GET /api/correlation/{station_id}
Matrice de corrélation entre les variables

**Response:**
```json
{
  "station_id": "STATION_01",
  "correlation_matrix": {
    "temperature_humidity": -0.45,
    "temperature_pressure": 0.32,
    "humidity_precipitation": 0.67,
    ...
  }
}
```

#### 6. GET /api/files
Liste tous les fichiers disponibles dans Cloud Storage

**Query Parameters:**
- station_id : filtrer par station (optionnel)
- year : filtrer par année (optionnel)

**Response:**
```json
{
  "files": [
    {
      "name": "weather_20240101_120000.csv",
      "size_bytes": 52341,
      "upload_date": "2024-01-01T12:00:00Z",
      "station_id": "STATION_01",
      "records": 365
    }
  ],
  "total_files": 12
}
```

## Structure du Code

### Structure des Dossiers

```
weather-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── storage_handler.py
│   ├── data_processor.py
│   ├── validators.py
│   └── models.py
├── tests/
│   ├── test_api.py
│   ├── test_processor.py
│   └── sample_data.csv
├── Dockerfile
├── requirements.txt
├── cloudbuild.yaml
└── README.md
```

### app/storage_handler.py

```python
from google.cloud import storage
from datetime import datetime
import os

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
            df = pd.read_csv(pd.StringIO(content))
            dfs.append(df)
        
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        return pd.DataFrame()
```

### app/data_processor.py

```python
import pandas as pd
import numpy as np
from datetime import datetime

class WeatherDataProcessor:
    def __init__(self, df):
        """
        Initialise le processeur avec un DataFrame pandas
        """
        self.df = df.copy()
        self._prepare_data()
    
    def _prepare_data(self):
        """Prépare les données : conversion de types, tri, etc."""
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.sort_values('date')
        
        # Colonnes numériques
        self.numeric_columns = ['temperature', 'humidity', 'pressure', 
                                'wind_speed', 'precipitation']
    
    def get_global_statistics(self, start_date=None, end_date=None):
        """Calcule les statistiques globales"""
        df = self._filter_by_date(start_date, end_date)
        
        stats = {}
        for col in self.numeric_columns:
            stats[col] = {
                'mean': float(df[col].mean()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'std': float(df[col].std()),
                'median': float(df[col].median())
            }
        
        stats['total_precipitation'] = float(df['precipitation'].sum())
        stats['records_count'] = len(df)
        
        return stats
    
    def get_monthly_summary(self, year):
        """Résumé mensuel pour une année"""
        df = self.df[self.df['date'].dt.year == year]
        
        monthly = df.groupby(df['date'].dt.month).agg({
            'temperature': 'mean',
            'precipitation': 'sum',
            'humidity': 'mean',
            'wind_speed': 'mean'
        }).round(2)
        
        # Compter les jours de pluie
        rain_days = df[df['precipitation'] > 0].groupby(
            df['date'].dt.month
        ).size()
        
        result = []
        for month in range(1, 13):
            if month in monthly.index:
                result.append({
                    'month': month,
                    'avg_temperature': float(monthly.loc[month, 'temperature']),
                    'total_precipitation': float(monthly.loc[month, 'precipitation']),
                    'avg_humidity': float(monthly.loc[month, 'humidity']),
                    'avg_wind_speed': float(monthly.loc[month, 'wind_speed']),
                    'days_with_rain': int(rain_days.get(month, 0))
                })
        
        return result
    
    def detect_anomalies(self, threshold=3):
        """
        Détecte les anomalies en utilisant le z-score
        threshold: nombre d'écarts-types pour considérer une valeur comme anomale
        """
        anomalies = []
        
        for col in self.numeric_columns:
            mean = self.df[col].mean()
            std = self.df[col].std()
            
            z_scores = np.abs((self.df[col] - mean) / std)
            anomaly_mask = z_scores > threshold
            
            anomaly_records = self.df[anomaly_mask]
            
            for idx, row in anomaly_records.iterrows():
                z_score = z_scores[idx]
                anomalies.append({
                    'date': row['date'].strftime('%Y-%m-%d'),
                    'variable': col,
                    'value': float(row[col]),
                    'mean': float(mean),
                    'std': float(std),
                    'z_score': float(z_score),
                    'severity': 'high' if z_score > 4 else 'medium'
                })
        
        return sorted(anomalies, key=lambda x: x['z_score'], reverse=True)
    
    def get_correlation_matrix(self):
        """Calcule la matrice de corrélation"""
        corr = self.df[self.numeric_columns].corr()
        
        result = {}
        for i, col1 in enumerate(self.numeric_columns):
            for col2 in self.numeric_columns[i+1:]:
                key = f"{col1}_{col2}"
                result[key] = round(float(corr.loc[col1, col2]), 3)
        
        return result
    
    def _filter_by_date(self, start_date=None, end_date=None):
        """Filtre le DataFrame par dates"""
        df = self.df.copy()
        
        if start_date:
            df = df[df['date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['date'] <= pd.to_datetime(end_date)]
        
        return df
```

### app/validators.py

```python
import pandas as pd
from werkzeug.datastructures import FileStorage

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
            
            df = pd.read_csv(pd.StringIO(content.decode('utf-8')))
            
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
```

### app/main.py

```python
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import pandas as pd

from .storage_handler import WeatherStorageHandler
from .data_processor import WeatherDataProcessor
from .validators import DataValidator

app = Flask(__name__)

BUCKET_NAME = os.getenv('BUCKET_NAME')
storage_handler = WeatherStorageHandler(BUCKET_NAME)

@app.route('/')
def home():
    return jsonify({
        'name': 'Weather Data Analysis API',
        'version': '1.0.0',
        'endpoints': [
            '/api/upload',
            '/api/statistics/{station_id}',
            '/api/monthly-summary/{station_id}/{year}',
            '/api/anomalies/{station_id}',
            '/api/correlation/{station_id}',
            '/api/files'
        ]
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/upload', methods=['POST'])
def upload_data():
    """Upload un fichier CSV de données météorologiques"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    station_id = request.form.get('station_id', 'unknown')
    
    # Validation
    is_valid, result = DataValidator.validate_csv_file(file)
    if not is_valid:
        return jsonify({'error': result}), 400
    
    df = result
    
    # Upload vers Cloud Storage
    file.seek(0)
    content = file.read().decode('utf-8')
    blob_path, filename = storage_handler.upload_file(
        content, station_id, secure_filename(file.filename)
    )
    
    return jsonify({
        'status': 'success',
        'file_name': filename,
        'records_count': len(df),
        'storage_path': blob_path,
        'upload_timestamp': pd.Timestamp.now().isoformat()
    }), 201

@app.route('/api/statistics/<station_id>', methods=['GET'])
def get_statistics(station_id):
    """Statistiques globales pour une station"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Récupérer les données
    df = storage_handler.get_all_data_for_station(station_id)
    
    if df.empty:
        return jsonify({'error': 'No data found for this station'}), 404
    
    processor = WeatherDataProcessor(df)
    stats = processor.get_global_statistics(start_date, end_date)
    
    return jsonify({
        'station_id': station_id,
        'period': {
            'start': start_date or df['date'].min().strftime('%Y-%m-%d'),
            'end': end_date or df['date'].max().strftime('%Y-%m-%d')
        },
        'statistics': stats
    })

@app.route('/api/monthly-summary/<station_id>/<int:year>', methods=['GET'])
def get_monthly_summary(station_id, year):
    """Résumé mensuel pour une année"""
    df = storage_handler.get_all_data_for_station(station_id)
    
    if df.empty:
        return jsonify({'error': 'No data found'}), 404
    
    processor = WeatherDataProcessor(df)
    summary = processor.get_monthly_summary(year)
    
    return jsonify({
        'station_id': station_id,
        'year': year,
        'monthly_data': summary
    })

@app.route('/api/anomalies/<station_id>', methods=['GET'])
def detect_anomalies(station_id):
    """Détection d'anomalies"""
    threshold = float(request.args.get('threshold', 3))
    
    df = storage_handler.get_all_data_for_station(station_id)
    
    if df.empty:
        return jsonify({'error': 'No data found'}), 404
    
    processor = WeatherDataProcessor(df)
    anomalies = processor.detect_anomalies(threshold)
    
    return jsonify({
        'station_id': station_id,
        'threshold': threshold,
        'anomalies': anomalies,
        'total_anomalies': len(anomalies)
    })

@app.route('/api/correlation/<station_id>', methods=['GET'])
def get_correlation(station_id):
    """Matrice de corrélation"""
    df = storage_handler.get_all_data_for_station(station_id)
    
    if df.empty:
        return jsonify({'error': 'No data found'}), 404
    
    processor = WeatherDataProcessor(df)
    correlation = processor.get_correlation_matrix()
    
    return jsonify({
        'station_id': station_id,
        'correlation_matrix': correlation
    })

@app.route('/api/files', methods=['GET'])
def list_files():
    """Liste les fichiers disponibles"""
    station_id = request.args.get('station_id')
    year = request.args.get('year', type=int)
    
    files = storage_handler.list_files(station_id=station_id, year=year)
    
    return jsonify({
        'files': files,
        'total_files': len(files)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
```

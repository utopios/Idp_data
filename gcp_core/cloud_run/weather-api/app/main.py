from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import pandas as pd

from storage_handler import WeatherStorageHandler
from data_processor import WeatherDataProcessor
from validators import DataValidator

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
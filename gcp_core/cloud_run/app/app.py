from flask import Flask, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Bienvenue sur mon API Cloud Run',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify({
        'received': data,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/env')
def env_vars():
    """Affiche les variables d'environnement (pour démo)"""
    return jsonify({
        'PROJECT_ID': os.getenv('GCP_PROJECT', 'not-set'),
        'SERVICE': os.getenv('K_SERVICE', 'not-set'),
        'REVISION': os.getenv('K_REVISION', 'not-set')
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
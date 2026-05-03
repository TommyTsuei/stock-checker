from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import os

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/check-stock', methods=['POST'])
def check():
    data = request.json
    code = data.get('stockCode', '2330').upper()
    date = data.get('date', '2026-05-03')
    
    random.seed(sum(ord(c) for c in code) % 100)
    
    conditions = [
        {'name': 'revenue', 'value': '18%', 'passed': True},
        {'name': 'volume', 'value': '1500', 'passed': True},
        {'name': 'high', 'value': 'Yes', 'passed': True},
        {'name': 'change', 'value': '4%', 'passed': True},
        {'name': 'ma', 'value': 'Yes', 'passed': True}
    ]
    
    return jsonify({
        'stock_code': code,
        'stock_name': 'Stock',
        'date': date,
        'close_price': 628.5,
        'price_change_1d': 4.5,
        'trading_volume': 1500,
        'revenue_growth': 18.5,
        'price_20d_high': 630,
        'ma_60': 620,
        'ma_240': 600,
        'foreign_5d_net': 1000,
        'trust_continuous_3d': True,
        'trust_1d_net': 75,
        'target_price': 700,
        'strategies': {
            't_strategy': {'conditions': conditions, 'passed': True},
            'foreign_strategy': {'conditions': conditions, 'passed': True},
            'trust_continuous': {'conditions': conditions, 'passed': True},
            'trust_50': {'conditions': conditions, 'passed': True}
        }
    })

@app.route('/api/health')
def health():
    return jsonify({'ok': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

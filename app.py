web: python app.py
#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import random
import os

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

def get_mock_stock_data(stock_code, date_str):
    seed = sum(ord(c) for c in stock_code) % 100
    random.seed(seed)
    return {
        'stock_code': stock_code,
        'stock_name': 'Stock',
        'revenue_growth': random.uniform(10, 25),
        'trading_volume': random.randint(800, 2000),
        'close_price': random.uniform(50, 800),
        'price_change_1d': random.uniform(-5, 8),
        'price_20d_high': random.uniform(50, 800),
        'ma_60': random.uniform(50, 800),
        'ma_240': random.uniform(50, 800),
        'foreign_5d_net': random.randint(-500, 2000),
        'trust_1d_net': random.randint(0, 200),
        'trust_continuous_3d': random.choice([True, False])
    }

def check_t_strategy(data):
    conditions = []
    cond1 = data['revenue_growth'] > 15
    conditions.append({'name': 'revenue_growth > 15', 'value': f"{data['revenue_growth']:.1f}", 'passed': cond1})
    cond2 = data['trading_volume'] > 1000
    conditions.append({'name': 'trading_volume > 1000', 'value': f"{data['trading_volume']}", 'passed': cond2})
    cond3 = data['close_price'] >= data['price_20d_high'] * 0.99
    conditions.append({'name': 'price_20d_high', 'value': 'Yes' if cond3 else 'No', 'passed': cond3})
    cond4 = data['price_change_1d'] > 3
    conditions.append({'name': 'price_change > 3', 'value': f"{data['price_change_1d']:.1f}", 'passed': cond4})
    cond5 = data['ma_60'] > data['ma_240']
    conditions.append({'name': 'ma_60 > ma_240', 'value': 'Yes' if cond5 else 'No', 'passed': cond5})
    passed = all([cond1, cond2, cond3, cond4, cond5])
    return {'conditions': conditions, 'passed': passed}

def check_foreign_strategy(t_strategy_result, data):
    conditions = t_strategy_result['conditions'].copy()
    cond6 = data['foreign_5d_net'] > 0
    conditions.append({'name': 'foreign > 0', 'value': f"{data['foreign_5d_net']}", 'passed': cond6})
    return {'conditions': conditions, 'passed': t_strategy_result['passed'] and cond6}

def check_trust_continuous_strategy(t_strategy_result, data):
    conditions = t_strategy_result['conditions'].copy()
    cond6 = data['trust_continuous_3d']
    conditions.append({'name': 'trust_continuous_3d', 'value': 'Yes' if cond6 else 'No', 'passed': cond6})
    return {'conditions': conditions, 'passed': t_strategy_result['passed'] and cond6}

def check_trust_50_strategy(t_strategy_result, data):
    conditions = t_strategy_result['conditions'].copy()
    cond6 = data['trust_1d_net'] > 50
    conditions.append({'name': 'trust > 50', 'value': f"{data['trust_1d_net']}", 'passed': cond6})
    return {'conditions': conditions, 'passed': t_strategy_result['passed'] and cond6}

@app.route('/api/check-stock', methods=['POST'])
def check_stock():
    try:
        request_data = request.json
        stock_code = request_data.get('stockCode', '').upper()
        date_str = request_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        if not stock_code:
            return jsonify({'error': 'missing code'}), 400
        stock_data = get_mock_stock_data(stock_code, date_str)
        t_strategy = check_t_strategy(stock_data)
        foreign_strategy = check_foreign_strategy(t_strategy, stock_data)
        trust_continuous = check_trust_continuous_strategy(t_strategy, stock_data)
        trust_50 = check_trust_50_strategy(t_strategy, stock_data)
        result = {
            'stock_code': stock_data['stock_code'],
            'stock_name': stock_data['stock_name'],
            'date': date_str,
            'close_price': round(stock_data['close_price'], 2),
            'price_change_1d': round(stock_data['price_change_1d'], 2),
            'trading_volume': stock_data['trading_volume'],
            'revenue_growth': round(stock_data['revenue_growth'], 1),
            'price_20d_high': round(stock_data['price_20d_high'], 2),
            'ma_60': round(stock_data['ma_60'], 2),
            'ma_240': round(stock_data['ma_240'], 2),
            'foreign_5d_net': stock_data['foreign_5d_net'],
            'trust_continuous_3d': stock_data['trust_continuous_3d'],
            'trust_1d_net': stock_data['trust_1d_net'],
            'target_price': round(stock_data['close_price'] * random.uniform(1.05, 1.15), 2),
            'strategies': {
                't_strategy': t_strategy,
                'foreign_strategy': foreign_strategy,
                'trust_continuous': trust_continuous,
                'trust_50': trust_50
            }
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
Flask==2.3.2
flask-cors==4.0.0
Werkzeug==2.3.6

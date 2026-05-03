from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Stock Checker</title></head>
    <body><h1>Stock Checker Running!</h1></body>
    </html>
    '''

@app.route('/api/check-stock', methods=['POST'])
def check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='../static')

# Your API key (put the correct one)
API_KEY = 'af5e9e01462300ccb2ca7b31'

def get_exchange_rate(base_currency, target_currency, api_key):
    """Fetches the exchange rate from the API."""
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and 'conversion_rates' in data:
        return data['conversion_rates'].get(target_currency, None)
    else:
        return None

@app.route('/convert', methods=['GET'])
def convert_currency():
    """API endpoint for converting currency"""
    amount = float(request.args.get('amount'))
    base_currency = request.args.get('base_currency')
    target_currency = request.args.get('target_currency')

    # Get the exchange rate
    rate = get_exchange_rate(base_currency, target_currency, API_KEY)

    if rate:
        result = amount * rate
        return jsonify({'success': True, 'result': result})
    else:
        return jsonify({'success': False, 'error': 'Unable to get exchange rate'}), 400

@app.route('/')
def serve_index():
    return send_from_directory('../static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)

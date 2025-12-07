from flask import Flask, render_template, request, jsonify
# OPTION 1: Use Alpha Vantage (more reliable)
from utils.data_fetcher_alphavantage import fetch_stock_data, get_available_stocks, validate_stock, check_api_key
# OPTION 2: Use Yahoo Finance (uncomment line below if you want to use Yahoo instead)
# from utils.data_fetcher import fetch_stock_data, get_available_stocks, validate_stock

from utils.preprocessor import preprocess_data
from models.arima_model import predict_arima
from models.lstm_model import predict_lstm
from models.prophet_model import predict_prophet
from models.ensemble import ensemble_predictions
import traceback

app = Flask(__name__)

# Popular stocks list
POPULAR_STOCKS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'V', 'WMT',
    'JNJ', 'PG', 'UNH', 'HD', 'BAC', 'MA', 'DIS', 'ADBE', 'NFLX', 'CRM',
    'CSCO', 'INTC', 'PFE', 'VZ', 'KO', 'NKE', 'T', 'MRK', 'ABT', 'PEP',
    'COST', 'TMO', 'AVGO', 'TXN', 'LLY', 'ORCL', 'ACN', 'CVX', 'NEE', 'DHR',
    'QCOM', 'MDT', 'BMY', 'HON', 'UNP', 'LIN', 'PM', 'RTX', 'LOW', 'AMD'
]

@app.route('/')
def index():
    return render_template('index.html', stocks=POPULAR_STOCKS)

@app.route('/search_stock', methods=['POST'])
def search_stock():
    """Validate if a stock symbol is available"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').upper().strip()
        
        if not symbol:
            return jsonify({'success': False, 'message': 'Please enter a stock symbol'})
        
        is_valid, message = validate_stock(symbol)
        
        return jsonify({
            'success': is_valid,
            'message': message,
            'symbol': symbol
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').upper().strip()
        
        if not symbol:
            return jsonify({'success': False, 'message': 'Please select a stock'})
        
        # Step 1: Fetch stock data
        print(f"Fetching data for {symbol}...")
        # Note: Alpha Vantage uses 'outputsize' parameter, not 'period'
        stock_data = fetch_stock_data(symbol, outputsize='full')
        
        if stock_data is None:
            return jsonify({
                'success': False,
                'message': f'Could not fetch data for {symbol}. Please try another stock or check your API key/internet connection.'
            })
        
        if len(stock_data) < 100:
            return jsonify({
                'success': False,
                'message': f'Insufficient data for {symbol}. Only {len(stock_data)} days available. Need at least 100 days.'
            })
        
        # Step 2: Preprocess data
        print("Preprocessing data...")
        processed_data = preprocess_data(stock_data)
        
        # Step 3: Get current price
        current_high = float(stock_data['High'].iloc[-1])
        current_low = float(stock_data['Low'].iloc[-1])
        
        # Step 4: Run predictions from all models
        print("Running ARIMA model...")
        arima_high, arima_low = predict_arima(processed_data)
        
        print("Running LSTM model...")
        lstm_high, lstm_low = predict_lstm(processed_data)
        
        print("Running Prophet model...")
        prophet_high, prophet_low = predict_prophet(processed_data)
        
        # Step 5: Ensemble predictions
        print("Combining predictions...")
        final_high, final_low = ensemble_predictions(
            arima_high, arima_low,
            lstm_high, lstm_low,
            prophet_high, prophet_low
        )
        
        # Step 6: Format response
        predictions = []
        for i in range(7):
            predictions.append({
                'day': i + 1,
                'high': round(final_high[i], 2),
                'low': round(final_low[i], 2)
            })
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'current_high': round(current_high, 2),
            'current_low': round(current_low, 2),
            'predictions': predictions
        })
        
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Prediction failed: {str(e)}'
        })

if __name__ == '__main__':
    print("=" * 50)
    print(" Stock Price Prediction System Starting...")
    print("=" * 50)
    
    # Check API key
    is_valid, message = check_api_key()
    if is_valid:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")
        print("Get your FREE API key from: https://www.alphavantage.co/support/#api-key")
        print("Then update API_KEY in utils/data_fetcher_alphavantage.py")
    
    print("Server running at: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
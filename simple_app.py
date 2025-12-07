#!/usr/bin/env python3
"""
Simple Stock Price Prediction API
Run with: python simple_app.py
Access at: http://localhost:8080
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
from datetime import datetime, timedelta

print("Starting import of standard libraries...")
# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Importing project utils...")
# Use yfinance instead of Alpha Vantage
from utils.data_fetcher import fetch_stock_data, validate_stock
# from utils.data_fetcher_alphavantage import fetch_stock_data, validate_stock, check_api_key
def check_api_key(): return True, "Using Yahoo Finance (No API Key needed)"
from utils.preprocessor import preprocess_data

print("Importing models (this may take a while)...")
print("Importing ARIMA...")
from models.arima_model import predict_arima
# print("Importing LSTM (TensorFlow)...")
# from models.lstm_model import predict_lstm
print("Skipping LSTM (TensorFlow) to avoid hang...")
predict_lstm = None
print("Importing Prophet...")
from models.prophet_model import predict_prophet
print("Importing Ensemble...")
from models.ensemble import ensemble_predictions

print("Imports complete. Starting Flask app...")

app = Flask(__name__, static_folder='frontend_simple', static_url_path='')
CORS(app)  # Enable CORS for frontend

# Nifty 50 stocks (Yahoo Finance symbols usually end with .NS for NSE)
STOCKS = [
    'ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS',
    'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'BHARTIARTL.NS',
    'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'DIVISLAB.NS', 'DRREDDY.NS',
    'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS',
    'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ITC.NS',
    'INDUSINDBK.NS', 'INFY.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LTIM.NS',
    'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NTPC.NS', 'NESTLEIND.NS',
    'ONGC.NS', 'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SBIN.NS',
    'SUNPHARMA.NS', 'TCS.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS',
    'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'WIPRO.NS'
]

@app.route('/')
def home():
    """Serve the main HTML page"""
    return send_from_directory('frontend_simple', 'index.html')

@app.route('/api/validate/<symbol>')
def validate(symbol):
    """Validate a stock symbol"""
    try:
        is_valid, message = validate_stock(symbol.upper())
        return jsonify({'valid': is_valid, 'message': message})
    except Exception as e:
        return jsonify({'valid': False, 'message': str(e)}), 500

@app.route('/api/predict/<symbol>')
def predict(symbol):
    """Predict stock prices for the next 7 days"""
    try:
        symbol = symbol.upper()
        
        # Fetch data
        print(f"Fetching data for {symbol}...")
        data = fetch_stock_data(symbol)
        if data is None or len(data) < 100:
            return jsonify({'error': 'Insufficient data'}), 400
        
        # Preprocess
        print("Preprocessing...")
        processed = preprocess_data(data)
        
        # Get current prices
        current_high = float(data['High'].iloc[-1])
        current_low = float(data['Low'].iloc[-1])
        
        # Run models
        print("Running ARIMA...")
        arima_h, arima_l = predict_arima(processed, 7)
        
        print("Skipping LSTM...")
        # lstm_h, lstm_l = predict_lstm(processed, 7)
        # Use ARIMA results as fallback for LSTM
        lstm_h, lstm_l = arima_h, arima_l
        
        print("Running Prophet...")
        prophet_h, prophet_l = predict_prophet(processed, 7)
        
        # Ensemble
        print("Combining predictions...")
        final_h, final_l = ensemble_predictions(
            arima_h, arima_l,
            lstm_h, lstm_l,
            prophet_h, prophet_l
        )
        
        # Format response with actual dates
        predictions = []
        last_date = data['Date'].iloc[-1]
        
        for i in range(7):
            # Calculate future date (skip weekends for trading days)
            future_date = last_date + timedelta(days=i+1)
            
            predictions.append({
                'day': i + 1,
                'date': future_date.strftime('%Y-%m-%d'),
                'date_formatted': future_date.strftime('%d %b %Y'),
                'high': round(float(final_h[i]), 2),
                'low': round(float(final_l[i]), 2)
            })
        
        return jsonify({
            'symbol': symbol,
            'current': {'high': round(current_high, 2), 'low': round(current_low, 2)},
            'predictions': predictions
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/stocks')
def get_stocks():
    """Get list of popular stocks"""
    return jsonify({'stocks': STOCKS})

if __name__ == '__main__':
    print("=" * 60)
    print(" StocX - AI Stock Price Prediction")
    print("=" * 60)
    
    # Check API key
    is_valid, msg = check_api_key()
    print(f"{msg}")
    
    print("\nServer starting at: http://localhost:8082")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=8083, debug=True)

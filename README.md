# Stock Price Prediction System

A full-stack ML platform for stock price prediction using an ensemble of ARIMA, LSTM, and Facebook Prophet models. Predicts the next 7 days' high and low prices for popular stocks.

## Features

- **Ensemble ML Models**: Combines ARIMA (statistical), LSTM (deep learning), and Prophet (time series) for accurate predictions
- **Real-time Data**: Fetches 2-3 years of historical market data using yfinance API
- **50+ Stocks Supported**: Pre-configured with popular US and Indian stocks (Nifty 50)
- **Web Interface**: Simple, clean UI to select stocks and view predictions
- **No API Key Required**: Uses free yfinance API with no authentication needed

## What this project does

- Fetches historical stock data using **yfinance API** (Yahoo Finance)
- Preprocesses and validates data with robust error handling
- Runs three prediction models: ARIMA, LSTM, and Prophet
- Combines model outputs using weighted ensemble methodology
- Provides a web interface to view current prices and 7-day predictions

## Quick Requirements

- Python 3.10+ and `pip` installed
- Internet connection (for fetching stock data)
- Optional: Node.js and `npm` for React frontend

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. (Optional) Install Frontend Dependencies

For the React UI:

```bash
cd frontend
npm install
```

## Running the Application

### Simple Version (Recommended)

Run the simplified Flask app with built-in HTML frontend:

```bash
python simple_app.py
```

Then open your browser to `http://localhost:5000`

### Full Version

Run the full Flask backend:

```bash
python app.py
```

**Optional**: Run the React frontend in a separate terminal:

```bash
cd frontend
npm start
```

The React app will run on `http://localhost:3000` and connect to the backend at port `5000`.

## How to Use

1. Start the backend (`python simple_app.py` or `python app.py`)
2. Open your browser to `http://localhost:5000`
3. Select a stock from the dropdown or search for a ticker:
   - **US Stocks**: AAPL, MSFT, GOOGL, TSLA, etc.
   - **Indian Stocks**: RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, etc.
4. Click **Predict** to see:
   - Current high/low prices
   - 7-day predictions with interactive charts

## Stock Ticker Format

- **US Stocks**: Use ticker symbol directly (e.g., `AAPL`, `MSFT`)
- **Indian Stocks**: Add `.NS` suffix for NSE (e.g., `RELIANCE.NS`, `TCS.NS`)
- **Indian Stocks**: Add `.BO` suffix for BSE (e.g., `RELIANCE.BO`)

## Project Structure

```
stock-price-prediction/
├── app.py                 # Full Flask backend with API endpoints
├── simple_app.py          # Simplified Flask app (recommended)
├── requirements.txt       # Python dependencies
├── models/               # ML model implementations
│   ├── arima_model.py    # ARIMA statistical model
│   ├── lstm_model.py     # LSTM deep learning model
│   ├── prophet_model.py  # Facebook Prophet model
│   └── ensemble.py       # Ensemble combination logic
├── utils/                # Data fetching and preprocessing
│   ├── data_fetcher.py   # yfinance data fetcher
│   └── preprocessor.py   # Data preprocessing and validation
├── frontend/             # React UI (optional)
├── frontend_simple/      # Simple HTML frontend
├── static/               # CSS and JavaScript
└── templates/            # Flask HTML templates
```

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: React.js (optional), HTML/CSS/JavaScript
- **ML Models**: 
  - ARIMA (statsmodels)
  - LSTM (TensorFlow/Keras)
  - Facebook Prophet
- **Data Source**: yfinance API (Yahoo Finance)
- **Visualization**: Chart.js

## Notes & Troubleshooting

- **No API Key Required**: yfinance is free and doesn't require authentication
- **Data Availability**: yfinance provides reliable data for most stocks, but some may have limited history
- **Slow Predictions**: LSTM training can be slow; the app is optimized for speed with reduced epochs
- **Indian Stocks**: Use `.NS` suffix for NSE stocks (e.g., `RELIANCE.NS`)
- **Rate Limits**: yfinance has no strict rate limits, but avoid excessive requests

## Model Details

### ARIMA
- Automatic stationarity testing (ADF test)
- Optimal differencing order selection
- Parameters: (5, d, 2) where d is auto-selected

### LSTM
- 2-layer LSTM with dropout
- Optimized for speed (30 units, 15 epochs)
- Sequence length: 30 days

### Prophet
- Daily, weekly, and yearly seasonality
- Changepoint detection
- Robust to missing data

### Ensemble
- Weighted average: ARIMA (25%), LSTM (45%), Prophet (30%)
- Ensures logical predictions (High ≥ Low)

## Contributing

Feel free to open issues or submit pull requests. Contributions are welcome!

## License

This project is open source. Add a license file if you plan to distribute publicly.

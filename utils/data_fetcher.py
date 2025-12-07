import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def validate_stock(symbol):
    """
    Validate if a stock symbol exists and has sufficient data
    Returns: (is_valid, message)
    """
    try:
        ticker = yf.Ticker(symbol)
        
        # Try to get recent data
        hist = ticker.history(period='5d')
        
        if hist.empty:
            return False, f"No data found for symbol '{symbol}'. Please check the symbol."
        
        # Check if we have enough historical data (try 3 years to be safe)
        hist_long = ticker.history(period='3y')
        
        if len(hist_long) < 100:
            return False, f"Insufficient historical data for '{symbol}'. Need at least 100 days."
        
        # Get stock info
        try:
            info = ticker.info
            stock_name = info.get('longName', symbol)
        except:
            stock_name = symbol
        
        return True, f"✓ {stock_name} ({symbol}) - Data available"
        
    except Exception as e:
        return False, f"Error validating '{symbol}': {str(e)}"

def fetch_stock_data(symbol, period='3y'):
    """
    Fetch historical stock data from Yahoo Finance
    
    Parameters:
    - symbol: Stock ticker symbol (e.g., 'AAPL')
    - period: Data period (default: '3y' for 3 years)
    
    Returns:
    - pandas DataFrame with Date, Open, High, Low, Close, Volume
    """
    try:
        print(f"Fetching {period} of data for {symbol}...")
        
        # Create ticker object
        ticker = yf.Ticker(symbol)
        
        # Try different periods if first fails
        periods_to_try = ['3y', '2y', '1y', '6mo']
        data = None
        
        for period_attempt in periods_to_try:
            try:
                print(f"  Trying period: {period_attempt}")
                data = ticker.history(period=period_attempt)
                
                if not data.empty and len(data) >= 100:
                    print(f"  Successfully fetched {len(data)} days")
                    break
                else:
                    print(f"  Insufficient data with period {period_attempt}")
            except Exception as e:
                print(f"  Failed with period {period_attempt}: {str(e)}")
                continue
        
        if data is None or data.empty:
            print(f"No data found for {symbol}")
            return None
        
        if len(data) < 100:
            print(f"Insufficient data: only {len(data)} days available")
            return None
        
        # Reset index to make Date a column
        data.reset_index(inplace=True)
        
        # Keep only required columns
        required_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        available_cols = [col for col in required_cols if col in data.columns]
        data = data[available_cols]
        
        # Remove any NaN values
        data = data.dropna()
        
        # Ensure we still have enough data after cleaning
        if len(data) < 100:
            print(f"After cleaning: insufficient data ({len(data)} days)")
            return None
        
        print(f"✓ Successfully fetched and cleaned {len(data)} days of data for {symbol}")
        
        return data
        
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def get_available_stocks():
    """
    Returns list of popular stocks that are available
    This is a curated list of major stocks
    """
    return [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'V', 'WMT',
        'JNJ', 'PG', 'UNH', 'HD', 'BAC', 'MA', 'DIS', 'ADBE', 'NFLX', 'CRM',
        'CSCO', 'INTC', 'PFE', 'VZ', 'KO', 'NKE', 'T', 'MRK', 'ABT', 'PEP',
        'COST', 'TMO', 'AVGO', 'TXN', 'LLY', 'ORCL', 'ACN', 'CVX', 'NEE', 'DHR',
        'QCOM', 'MDT', 'BMY', 'HON', 'UNP', 'LIN', 'PM', 'RTX', 'LOW', 'AMD'
    ]

def get_stock_info(symbol):
    """
    Get basic information about a stock
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        return {
            'name': info.get('longName', symbol),
            'symbol': symbol,
            'sector': info.get('sector', 'Unknown'),
            'industry': info.get('industry', 'Unknown')
        }
    except:
        return {
            'name': symbol,
            'symbol': symbol,
            'sector': 'Unknown',
            'industry': 'Unknown'
        }
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

API_KEY = 'RWM4SZA7VCTW4X5J'  # Get free key from: https://www.alphavantage.co/support/#api-key
BASE_URL = 'https://www.alphavantage.co/query'

def validate_stock(symbol):
    """
    Validate if a stock symbol exists and has sufficient data
    Returns: (is_valid, message)
    """
    try:
        print(f"Validating {symbol}...")
        
        # Try to get recent quote
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': API_KEY
        }
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()
        
        # Check if we got valid data
        if 'Global Quote' in data and data['Global Quote']:
            quote = data['Global Quote']
            price = quote.get('05. price', None)
            
            if price:
                stock_name = quote.get('01. symbol', symbol)
                return True, f"✓ {stock_name} - Current price: ${float(price):.2f}"
            else:
                return False, f"No price data found for '{symbol}'"
        
        elif 'Note' in data:
            return False, "API rate limit reached. Please wait a minute and try again."
        
        elif 'Error Message' in data:
            return False, f"Invalid symbol '{symbol}'. Please check the ticker."
        
        else:
            return False, f"Could not validate '{symbol}'. Please try again."
        
    except Exception as e:
        return False, f"Error validating '{symbol}': {str(e)}"

def fetch_stock_data(symbol, outputsize='full'):
    """
    Fetch historical stock data from Alpha Vantage
    
    Parameters:
    - symbol: Stock ticker symbol (e.g., 'AAPL')
    - outputsize: 'compact' (100 days) or 'full' (20+ years)
    
    Returns:
    - pandas DataFrame with Date, Open, High, Low, Close, Volume
    """
    try:
        print(f"Fetching data for {symbol} from Alpha Vantage...")
        
        # API parameters
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': outputsize,  # 'full' gets 20+ years of data
            'apikey': API_KEY
        }
        
        # Make API request
        response = requests.get(BASE_URL, params=params, timeout=30)
        data = response.json()
        
        # Check for errors
        if 'Note' in data:
            print("⚠️ API rate limit reached (5 calls/min). Waiting 60 seconds...")
            time.sleep(60)
            # Retry once
            response = requests.get(BASE_URL, params=params, timeout=30)
            data = response.json()
        
        if 'Error Message' in data:
            print(f"✗ Error: {data['Error Message']}")
            return None
        
        if 'Time Series (Daily)' not in data:
            print(f"✗ No time series data found for {symbol}")
            print(f"Response: {data}")
            return None
        
        # Parse the time series data
        time_series = data['Time Series (Daily)']
        
        # Convert to DataFrame
        df = pd.DataFrame.from_dict(time_series, orient='index')
        
        # Rename columns
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        
        # Convert index to datetime
        df.index = pd.to_datetime(df.index)
        df.index.name = 'Date'
        
        # Reset index to make Date a column
        df.reset_index(inplace=True)
        
        # Convert price columns to float
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = df[col].astype(float)
        
        # Convert volume to int
        df['Volume'] = df['Volume'].astype(int)
        
        # Sort by date (oldest to newest)
        df = df.sort_values('Date').reset_index(drop=True)
        
        # Remove any NaN values
        df = df.dropna()
        
        print(f"✓ Successfully fetched {len(df)} days of data for {symbol}")
        
        return df
        
    except requests.exceptions.Timeout:
        print(f"✗ Request timeout for {symbol}")
        return None
    except Exception as e:
        print(f"✗ Error fetching data for {symbol}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def get_intraday_data(symbol, interval='5min', outputsize='compact'):
    """
    Fetch intraday (minute-level) data
    
    Parameters:
    - symbol: Stock ticker symbol
    - interval: '1min', '5min', '15min', '30min', '60min'
    - outputsize: 'compact' (100 datapoints) or 'full' (full day)
    
    Returns:
    - pandas DataFrame with intraday data
    """
    try:
        print(f"Fetching intraday data for {symbol}...")
        
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval,
            'outputsize': outputsize,
            'apikey': API_KEY
        }
        
        response = requests.get(BASE_URL, params=params, timeout=30)
        data = response.json()
        
        if f'Time Series ({interval})' not in data:
            print(f"No intraday data found")
            return None
        
        time_series = data[f'Time Series ({interval})']
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df.index = pd.to_datetime(df.index)
        df.index.name = 'DateTime'
        df.reset_index(inplace=True)
        
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = df[col].astype(float)
        df['Volume'] = df['Volume'].astype(int)
        
        df = df.sort_values('DateTime').reset_index(drop=True)
        
        return df
        
    except Exception as e:
        print(f"Error fetching intraday data: {str(e)}")
        return None

def get_available_stocks():
    """
    Returns list of popular stocks that work with Alpha Vantage
    """
    return [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'V', 'WMT',
        'JNJ', 'PG', 'UNH', 'HD', 'BAC', 'MA', 'DIS', 'ADBE', 'NFLX', 'CRM',
        'CSCO', 'INTC', 'PFE', 'VZ', 'KO', 'NKE', 'T', 'MRK', 'ABT', 'PEP',
        'COST', 'TMO', 'AVGO', 'TXN', 'LLY', 'ORCL', 'ACN', 'CVX', 'NEE', 'DHR',
        'QCOM', 'MDT', 'BMY', 'HON', 'UNP', 'LIN', 'PM', 'RTX', 'LOW', 'AMD',
        'IBM', 'GE', 'F', 'GM', 'BA', 'CAT', 'XOM', 'CVS', 'WFC', 'C'
    ]

def get_stock_info(symbol):
    """
    Get company overview information
    """
    try:
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol,
            'apikey': API_KEY
        }
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()
        
        if 'Symbol' in data:
            return {
                'name': data.get('Name', symbol),
                'symbol': symbol,
                'sector': data.get('Sector', 'Unknown'),
                'industry': data.get('Industry', 'Unknown'),
                'description': data.get('Description', ''),
                'exchange': data.get('Exchange', ''),
                'market_cap': data.get('MarketCapitalization', 'N/A')
            }
        else:
            return {
                'name': symbol,
                'symbol': symbol,
                'sector': 'Unknown',
                'industry': 'Unknown'
            }
    except:
        return {
            'name': symbol,
            'symbol': symbol,
            'sector': 'Unknown',
            'industry': 'Unknown'
        }

def check_api_key():
    """
    Check if API key is valid
    """
    if API_KEY == 'YOUR_API_KEY_HERE':
        return False, "⚠️ Please set your Alpha Vantage API key in data_fetcher_alphavantage.py"
    
    try:
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': 'AAPL',
            'apikey': API_KEY
        }
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()
        
        if 'Global Quote' in data:
            return True, "✓ API key is valid"
        elif 'Error Message' in data:
            return False, f"✗ API Error: {data['Error Message']}"
        elif 'Note' in data:
            return False, "⚠️ API rate limit reached"
        else:
            return False, "✗ Invalid API key"
            
    except Exception as e:
        return False, f"✗ Error checking API key: {str(e)}"
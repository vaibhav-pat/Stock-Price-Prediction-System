import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def preprocess_data(data):
    """
    Preprocess stock data for model training
    
    Parameters:
    - data: Raw stock data DataFrame
    
    Returns:
    - Dictionary with processed data for each model
    """
    
    df = data.copy()
    
    if len(df) > 500:
        df = df.tail(500)
        print(f"  Limited data to last {len(df)} days for faster processing")
    
    # Ensure Date is datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sort by date
    df = df.sort_values('Date')
    
    # Remove any duplicates
    df = df.drop_duplicates(subset=['Date'])
    
    # Reset index
    df = df.reset_index(drop=True)
    
    # Create features
    df['MA7'] = df['Close'].rolling(window=7, min_periods=1).mean()
    df['MA21'] = df['Close'].rolling(window=21, min_periods=1).mean()
    df['Volatility'] = df['Close'].rolling(window=10, min_periods=1).std()
    
    # Fill any NaN values with forward fill
    df = df.fillna(method='ffill')
    
    # Prepare data for different models
    processed = {
        'full_data': df,
        'dates': df['Date'].values,
        'high': df['High'].values,
        'low': df['Low'].values,
        'close': df['Close'].values,
        'volume': df['Volume'].values
    }
    
    # For LSTM - normalize data
    scaler_high = MinMaxScaler(feature_range=(0, 1))
    scaler_low = MinMaxScaler(feature_range=(0, 1))
    
    processed['high_scaled'] = scaler_high.fit_transform(df['High'].values.reshape(-1, 1))
    processed['low_scaled'] = scaler_low.fit_transform(df['Low'].values.reshape(-1, 1))
    processed['scaler_high'] = scaler_high
    processed['scaler_low'] = scaler_low
    
    # For Prophet - specific format
    processed['prophet_high'] = pd.DataFrame({
        'ds': df['Date'],
        'y': df['High']
    })
    
    processed['prophet_low'] = pd.DataFrame({
        'ds': df['Date'],
        'y': df['Low']
    })
    
    return processed

def create_sequences(data, sequence_length=60):
    """
    Create sequences for LSTM model
    
    Parameters:
    - data: Scaled data array
    - sequence_length: Number of time steps to look back
    
    Returns:
    - X, y arrays for training
    """
    X, y = [], []
    
    for i in range(sequence_length, len(data)):
        X.append(data[i-sequence_length:i, 0])
        y.append(data[i, 0])
    
    return np.array(X), np.array(y)

def inverse_transform_predictions(predictions, scaler):
    """
    Convert scaled predictions back to original scale
    """
    predictions = np.array(predictions).reshape(-1, 1)
    return scaler.inverse_transform(predictions).flatten()
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from utils.preprocessor import create_sequences, inverse_transform_predictions
import warnings
warnings.filterwarnings('ignore')

def build_lstm_model(sequence_length):
    """
    Build LSTM neural network architecture (OPTIMIZED FOR SPEED)
    """
    model = Sequential([
        LSTM(units=30, return_sequences=True, input_shape=(sequence_length, 1)),
        Dropout(0.2),
        LSTM(units=30, return_sequences=False),
        Dropout(0.2),
        Dense(units=15),
        Dense(units=1)
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def predict_lstm(processed_data, forecast_days=7, sequence_length=30):
    """
    Predict stock prices using LSTM model (OPTIMIZED VERSION)
    
    Parameters:
    - processed_data: Preprocessed data dictionary
    - forecast_days: Number of days to forecast (default: 7)
    - sequence_length: Number of previous days to consider (REDUCED to 30 for speed)
    
    Returns:
    - high_predictions: Array of predicted high prices
    - low_predictions: Array of predicted low prices
    """
    
    try:
        high_scaled = processed_data['high_scaled']
        low_scaled = processed_data['low_scaled']
        scaler_high = processed_data['scaler_high']
        scaler_low = processed_data['scaler_low']
        
        # Limit data for faster training
        max_data_points = 300  # Use only last 300 days
        if len(high_scaled) > max_data_points:
            high_scaled = high_scaled[-max_data_points:]
            low_scaled = low_scaled[-max_data_points:]
            print(f"  Limited LSTM training data to last {max_data_points} days for speed")
        
        # Predict High prices
        print("  Training LSTM for High prices...")
        X_high, y_high = create_sequences(high_scaled, sequence_length)
        
        if len(X_high) < 30:
            raise Exception("Insufficient data for LSTM training")
        
        X_high = X_high.reshape(X_high.shape[0], X_high.shape[1], 1)
        
        model_high = build_lstm_model(sequence_length)
        early_stop = EarlyStopping(monitor='loss', patience=3, restore_best_weights=True)
        
        model_high.fit(
            X_high, y_high,
            epochs=15,  # REDUCED from 50 to 15 for speed
            batch_size=16,  # INCREASED batch size for speed
            verbose=0,
            callbacks=[early_stop]
        )
        
        # Generate predictions
        last_sequence_high = high_scaled[-sequence_length:]
        high_predictions_scaled = []
        
        for _ in range(forecast_days):
            next_pred = model_high.predict(last_sequence_high.reshape(1, sequence_length, 1), verbose=0)
            high_predictions_scaled.append(next_pred[0, 0])
            last_sequence_high = np.append(last_sequence_high[1:], next_pred)
        
        high_predictions = inverse_transform_predictions(high_predictions_scaled, scaler_high)
        
        # Predict Low prices
        print("  Training LSTM for Low prices...")
        X_low, y_low = create_sequences(low_scaled, sequence_length)
        X_low = X_low.reshape(X_low.shape[0], X_low.shape[1], 1)
        
        model_low = build_lstm_model(sequence_length)
        model_low.fit(
            X_low, y_low,
            epochs=15,  # REDUCED from 50 to 15
            batch_size=16,  # INCREASED batch size
            verbose=0,
            callbacks=[early_stop]
        )
        
        last_sequence_low = low_scaled[-sequence_length:]
        low_predictions_scaled = []
        
        for _ in range(forecast_days):
            next_pred = model_low.predict(last_sequence_low.reshape(1, sequence_length, 1), verbose=0)
            low_predictions_scaled.append(next_pred[0, 0])
            last_sequence_low = np.append(last_sequence_low[1:], next_pred)
        
        low_predictions = inverse_transform_predictions(low_predictions_scaled, scaler_low)
        
        # Ensure High >= Low
        for i in range(len(high_predictions)):
            if high_predictions[i] < low_predictions[i]:
                high_predictions[i], low_predictions[i] = low_predictions[i], high_predictions[i]
        
        print(f"  ✓ LSTM predictions completed")
        
        return high_predictions, low_predictions
        
    except Exception as e:
        print(f"  ⚠ LSTM failed: {str(e)}")
        # Fallback to last known values
        last_high = processed_data['high'][-1]
        last_low = processed_data['low'][-1]
        
        high_predictions = np.full(forecast_days, last_high)
        low_predictions = np.full(forecast_days, last_low)
        
        return high_predictions, low_predictions
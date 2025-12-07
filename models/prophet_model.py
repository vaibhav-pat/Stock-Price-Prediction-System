import numpy as np
from prophet import Prophet
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def predict_prophet(processed_data, forecast_days=7):
    """
    Predict stock prices using Facebook Prophet
    
    Parameters:
    - processed_data: Preprocessed data dictionary
    - forecast_days: Number of days to forecast (default: 7)
    
    Returns:
    - high_predictions: Array of predicted high prices
    - low_predictions: Array of predicted low prices
    """
    
    try:
        df_high = processed_data['prophet_high'].copy()
        df_low = processed_data['prophet_low'].copy()
        
        # Predict High prices
        print("  Training Prophet for High prices...")
        model_high = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=True,
            changepoint_prior_scale=0.05
        )
        model_high.fit(df_high)
        
        future_high = model_high.make_future_dataframe(periods=forecast_days)
        forecast_high = model_high.predict(future_high)
        
        high_predictions = forecast_high['yhat'].tail(forecast_days).values
        
        # Predict Low prices
        print("  Training Prophet for Low prices...")
        model_low = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=True,
            changepoint_prior_scale=0.05
        )
        model_low.fit(df_low)
        
        future_low = model_low.make_future_dataframe(periods=forecast_days)
        forecast_low = model_low.predict(future_low)
        
        low_predictions = forecast_low['yhat'].tail(forecast_days).values
        
        # Ensure High >= Low
        for i in range(len(high_predictions)):
            if high_predictions[i] < low_predictions[i]:
                high_predictions[i], low_predictions[i] = low_predictions[i], high_predictions[i]
        
        # Ensure no negative predictions
        high_predictions = np.maximum(high_predictions, 0)
        low_predictions = np.maximum(low_predictions, 0)
        
        print(f"  ✓ Prophet predictions completed")
        
        return high_predictions, low_predictions
        
    except Exception as e:
        print(f"  ⚠ Prophet failed: {str(e)}")
        # Fallback to last known values
        last_high = processed_data['high'][-1]
        last_low = processed_data['low'][-1]
        
        high_predictions = np.full(forecast_days, last_high)
        low_predictions = np.full(forecast_days, last_low)
        
        return high_predictions, low_predictions
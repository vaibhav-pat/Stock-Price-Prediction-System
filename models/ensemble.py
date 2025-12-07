import numpy as np

def ensemble_predictions(arima_high, arima_low, lstm_high, lstm_low, prophet_high, prophet_low):
    """
    Combine predictions from multiple models using weighted average
    
    Parameters:
    - arima_high, arima_low: ARIMA predictions
    - lstm_high, lstm_low: LSTM predictions
    - prophet_high, prophet_low: Prophet predictions
    
    Returns:
    - final_high: Combined high price predictions
    - final_low: Combined low price predictions
    """
    
    # Weights for each model
    # These can be tuned based on historical accuracy
    weights = {
        'arima': 0.25,    # Traditional statistical model
        'lstm': 0.45,     # Deep learning - usually most accurate for time series
        'prophet': 0.30   # Good at capturing seasonality
    }
    
    # Combine High predictions
    final_high = (
        weights['arima'] * np.array(arima_high) +
        weights['lstm'] * np.array(lstm_high) +
        weights['prophet'] * np.array(prophet_high)
    )
    
    # Combine Low predictions
    final_low = (
        weights['arima'] * np.array(arima_low) +
        weights['lstm'] * np.array(lstm_low) +
        weights['prophet'] * np.array(prophet_low)
    )
    
    # Ensure High >= Low
    for i in range(len(final_high)):
        if final_high[i] < final_low[i]:
            # Average them if prediction is illogical
            avg = (final_high[i] + final_low[i]) / 2
            final_high[i] = avg * 1.01  # High slightly above average
            final_low[i] = avg * 0.99   # Low slightly below average
    
    return final_high, final_low

def voting_ensemble(arima_high, arima_low, lstm_high, lstm_low, prophet_high, prophet_low):
    """
    Alternative ensemble method: Take median of predictions
    (More robust to outliers)
    """
    
    final_high = []
    final_low = []
    
    for i in range(len(arima_high)):
        high_values = [arima_high[i], lstm_high[i], prophet_high[i]]
        low_values = [arima_low[i], lstm_low[i], prophet_low[i]]
        
        final_high.append(np.median(high_values))
        final_low.append(np.median(low_values))
    
    return np.array(final_high), np.array(final_low)

def adaptive_ensemble(arima_high, arima_low, lstm_high, lstm_low, prophet_high, prophet_low, 
                     historical_errors=None):
    """
    Adaptive ensemble: Adjust weights based on recent performance
    (Can be implemented with historical error tracking)
    """
    
    if historical_errors is None:
        # Default to weighted average if no error history
        return ensemble_predictions(arima_high, arima_low, lstm_high, lstm_low, 
                                   prophet_high, prophet_low)
    
    # Calculate weights inversely proportional to errors
    total_error = sum(historical_errors.values())
    
    if total_error == 0:
        weights = {'arima': 0.33, 'lstm': 0.34, 'prophet': 0.33}
    else:
        weights = {
            'arima': 1 - (historical_errors['arima'] / total_error),
            'lstm': 1 - (historical_errors['lstm'] / total_error),
            'prophet': 1 - (historical_errors['prophet'] / total_error)
        }
        
        # Normalize weights
        total_weight = sum(weights.values())
        weights = {k: v/total_weight for k, v in weights.items()}
    
    # Combine predictions
    final_high = (
        weights['arima'] * np.array(arima_high) +
        weights['lstm'] * np.array(lstm_high) +
        weights['prophet'] * np.array(prophet_high)
    )
    
    final_low = (
        weights['arima'] * np.array(arima_low) +
        weights['lstm'] * np.array(lstm_low) +
        weights['prophet'] * np.array(prophet_low)
    )
    
    return final_high, final_low
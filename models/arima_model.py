import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.filterwarnings('ignore')

def find_optimal_d(data, max_d=2, verbose=False):
    """
    Find the optimal differencing order (d) using Augmented Dickey-Fuller test
    
    Parameters:
    - data: Time series data (array or pandas Series)
    - max_d: Maximum d value to test (default: 2)
    - verbose: Print detailed output
    
    Returns:
    - d: Optimal differencing order (0, 1, or 2)
    
    Theory:
    -------
    The ADF (Augmented Dickey-Fuller) test checks if a time series is stationary:
    - H0 (Null Hypothesis): Series has a unit root (non-stationary)
    - H1 (Alternative): Series is stationary
    
    p-value < 0.05: Reject H0 → Series IS stationary
    p-value >= 0.05: Fail to reject H0 → Series is NOT stationary
    
    Differencing:
    - d=0: No differencing (use original series)
    - d=1: First difference (today - yesterday)
    - d=2: Second difference (diff of differences)
    """
    
    if verbose:
        print("\n" + "="*60)
        print("STATIONARITY TEST (ADF Test)")
        print("="*60)
    
    for d in range(max_d + 1):
        try:
            # Create differenced series
            if d == 0:
                test_series = data
                description = "Original Series"
            else:
                test_series = data.diff(d).dropna()
                description = f"Differenced Series (d={d})"
            
            # Perform ADF test
            adf_result = adfuller(test_series, autolag='AIC')
            
            # Extract results
            adf_statistic = adf_result[0]
            p_value = adf_result[1]
            critical_values = adf_result[4]
            
            if verbose:
                print(f"\nd={d}: {description}")
                print(f"  ADF Statistic: {adf_statistic:.6f}")
                print(f"  p-value: {p_value:.6f}")
                print(f"  Critical Values:")
                for key, value in critical_values.items():
                    print(f"    {key}: {value:.3f}")
            
            # Check if stationary (p-value < 0.05)
            if p_value < 0.05:
                if verbose:
                    print(f"\n✓ STATIONARY at d={d} (p-value = {p_value:.6f} < 0.05)")
                    print("="*60)
                return d
            else:
                if verbose:
                    print(f"  NOT stationary (p-value = {p_value:.6f} >= 0.05)")
        
        except Exception as e:
            if verbose:
                print(f"Error testing d={d}: {str(e)}")
            continue
    
    if verbose:
        print(f"\n⚠ Could not achieve stationarity. Using d={max_d}")
        print("="*60)
    
    return max_d

def predict_arima(processed_data, forecast_days=7, verbose=False):
    """
    Predict stock prices using ARIMA with automatic optimal d selection
    
    Parameters:
    - processed_data: Preprocessed data dictionary
    - forecast_days: Number of days to forecast (default: 7)
    - verbose: Print stationarity test details
    
    Returns:
    - high_predictions: Array of predicted high prices
    - low_predictions: Array of predicted low prices
    """
    
    try:
        high_data = processed_data['high']
        low_data = processed_data['low']
        
        print("\n" + "="*70)
        print("ARIMA MODEL - PREDICTING HIGH PRICES")
        print("="*70)
        
        # Find optimal d for HIGH prices
        print("\nTesting stationarity for HIGH prices...")
        d_high = find_optimal_d(high_data, max_d=2, verbose=verbose)
        print(f"Optimal d for HIGH: {d_high}")
        
        print("\n" + "="*70)
        print("ARIMA MODEL - PREDICTING LOW PRICES")
        print("="*70)
        
        # Find optimal d for LOW prices
        print("\nTesting stationarity for LOW prices...")
        d_low = find_optimal_d(low_data, max_d=2, verbose=verbose)
        print(f"Optimal d for LOW: {d_low}")
        
        # ARIMA parameters
        # p: Autoregressive order (lag observations)
        # d: Differencing order (found automatically)
        # q: Moving average order
        p = 5
        q = 2
        
        print("\n" + "="*70)
        print("TRAINING ARIMA MODELS")
        print("="*70)
        
        # Predict High prices with optimal d
        print(f"\nTraining ARIMA({p}, {d_high}, {q}) for HIGH prices...")
        order_high = (p, d_high, q)
        model_high = ARIMA(high_data, order=order_high)
        fitted_high = model_high.fit()
        
        if verbose:
            print(fitted_high.summary())
        
        high_predictions = fitted_high.forecast(steps=forecast_days)
        print(f"✓ HIGH predictions generated: {high_predictions}")
        
        # Predict Low prices with optimal d
        print(f"\nTraining ARIMA({p}, {d_low}, {q}) for LOW prices...")
        order_low = (p, d_low, q)
        model_low = ARIMA(low_data, order=order_low)
        fitted_low = model_low.fit()
        
        if verbose:
            print(fitted_low.summary())
        
        low_predictions = fitted_low.forecast(steps=forecast_days)
        print(f"✓ LOW predictions generated: {low_predictions}")
        
        # Ensure predictions are logical (High >= Low)
        for i in range(len(high_predictions)):
            if high_predictions[i] < low_predictions[i]:
                # Swap if prediction is illogical
                high_predictions[i], low_predictions[i] = low_predictions[i], high_predictions[i]
        
        print(f"\n✓ ARIMA predictions completed successfully")
        print("="*70)
        
        return high_predictions, low_predictions
        
    except Exception as e:
        print(f"✗ ARIMA failed: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Fallback: return simple moving average
        last_high = processed_data['high'][-1]
        last_low = processed_data['low'][-1]
        
        high_predictions = np.full(forecast_days, last_high)
        low_predictions = np.full(forecast_days, last_low)
        
        return high_predictions, low_predictions

def get_arima_diagnostics(data, d):
    """
    Get diagnostic information about ARIMA model fit
    
    Useful for understanding model quality:
    - AIC (Akaike Information Criterion): Lower is better
    - BIC (Bayesian Information Criterion): Lower is better
    - Log-Likelihood: Higher is better
    """
    
    try:
        model = ARIMA(data, order=(5, d, 2))
        fitted = model.fit()
        
        return {
            'aic': fitted.aic,
            'bic': fitted.bic,
            'llf': fitted.llf,
            'd': d,
            'summary': str(fitted.summary())
        }
    except Exception as e:
        print(f"Error getting diagnostics: {str(e)}")
        return None

# Example usage (for testing):
if __name__ == "__main__":
    import pandas as pd
    from utils.data_fetcher_alphavantage import fetch_stock_data
    from utils.preprocessor import preprocess_data
    
    # Fetch and preprocess data
    data = fetch_stock_data('AAPL')
    processed = preprocess_data(data)
    
    # Test ARIMA with stationarity checks
    high_pred, low_pred = predict_arima(processed, forecast_days=7, verbose=True)
    
    print("\nFinal Predictions:")
    print(f"High: {high_pred}")
    print(f"Low: {low_pred}")
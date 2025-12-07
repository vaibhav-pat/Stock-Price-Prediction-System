import React, { useState } from 'react';
import axios from 'axios';
import Header from './components/Header';
import StockSelector from './components/StockSelector';
import LoadingSpinner from './components/LoadingSpinner';
import Results from './components/Results';

// Popular stocks list
const POPULAR_STOCKS = [
  'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'V', 'WMT',
  'JNJ', 'PG', 'UNH', 'HD', 'BAC', 'MA', 'DIS', 'ADBE', 'NFLX', 'CRM',
  'CSCO', 'INTC', 'PFE', 'VZ', 'KO', 'NKE', 'T', 'MRK', 'ABT', 'PEP',
  'COST', 'TMO', 'AVGO', 'TXN', 'LLY', 'ORCL', 'ACN', 'CVX', 'NEE', 'DHR',
  'QCOM', 'MDT', 'BMY', 'HON', 'UNP', 'LIN', 'PM', 'RTX', 'LOW', 'AMD'
];

// API base URL - change this if your Flask runs on different port
const API_BASE_URL = 'http://localhost:5000';

function App() {
  const [selectedSymbol, setSelectedSymbol] = useState('');
  const [isValidSymbol, setIsValidSymbol] = useState(false);
  const [validationMessage, setValidationMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [predictions, setPredictions] = useState(null);
  const [error, setError] = useState('');

  // Handle stock selection from dropdown
  const handleStockSelect = (symbol) => {
    setSelectedSymbol(symbol);
    setIsValidSymbol(true);
    setValidationMessage('Stock selected');
    setError('');
  };

  // Validate custom stock symbol
  const validateStock = async (symbol) => {
    if (!symbol) {
      setError('Please enter a stock symbol');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_BASE_URL}/search_stock`, {
        symbol: symbol.toUpperCase()
      });

      if (response.data.success) {
        setSelectedSymbol(symbol.toUpperCase());
        setIsValidSymbol(true);
        setValidationMessage(response.data.message);
      } else {
        setIsValidSymbol(false);
        setValidationMessage(response.data.message);
      }
    } catch (err) {
      setError('Error validating stock. Please try again.');
      setIsValidSymbol(false);
    } finally {
      setIsLoading(false);
    }
  };

  // Get predictions
  const predictStock = async () => {
    if (!selectedSymbol) {
      setError('Please select a stock first');
      return;
    }

    setIsLoading(true);
    setError('');
    setPredictions(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/predict`, {
        symbol: selectedSymbol
      });

      if (response.data.success) {
        setPredictions(response.data);
      } else {
        setError(response.data.message || 'Prediction failed');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Error making prediction. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-4 md:p-6">
      <div className="max-w-7xl mx-auto">
        <Header />
        
        <div className="bg-white rounded-2xl shadow-2xl p-6 md:p-10">
          <StockSelector
            stocks={POPULAR_STOCKS}
            selectedSymbol={selectedSymbol}
            isValidSymbol={isValidSymbol}
            validationMessage={validationMessage}
            onStockSelect={handleStockSelect}
            onValidateStock={validateStock}
            onPredict={predictStock}
            isLoading={isLoading}
          />

          {error && (
            <div className="mt-6 bg-red-50 border-l-4 border-red-500 p-4 rounded">
              <p className="text-red-700 font-medium">{error}</p>
            </div>
          )}

          {isLoading && <LoadingSpinner />}

          {predictions && !isLoading && (
            <Results predictions={predictions} />
          )}
        </div>

        <footer className="text-center text-white mt-8 py-6">
          <p className="text-lg font-semibold">
            Powered by ARIMA, LSTM & Prophet | Alpha Vantage API
          </p>
          <p className="text-sm mt-2 opacity-90">
            Built with React.js, Tailwind CSS, TensorFlow & Flask
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
import React from 'react';

const Header = () => {
  return (
    <header className="bg-white rounded-2xl shadow-2xl p-8 mb-8 text-center">
      <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-3">
        📊 Stock Price Prediction System
      </h1>
      <p className="text-lg md:text-xl text-gray-600">
        AI-powered predictions using ARIMA, LSTM & Prophet models
      </p>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
        <div className="bg-green-50 p-4 rounded-xl border-2 border-green-200 hover:shadow-md transition-shadow">
          <div className="text-green-600 text-2xl mb-2">✓</div>
          <div className="text-sm font-semibold text-gray-700">No Authentication</div>
          <div className="text-xs text-gray-600">Direct prediction access</div>
        </div>
        
        <div className="bg-blue-50 p-4 rounded-xl border-2 border-blue-200 hover:shadow-md transition-shadow">
          <div className="text-blue-600 text-2xl mb-2">📡</div>
          <div className="text-sm font-semibold text-gray-700">Real-time Data</div>
          <div className="text-xs text-gray-600">Alpha Vantage API</div>
        </div>
        
        <div className="bg-purple-50 p-4 rounded-xl border-2 border-purple-200 hover:shadow-md transition-shadow">
          <div className="text-purple-600 text-2xl mb-2">🧠</div>
          <div className="text-sm font-semibold text-gray-700">Ensemble ML</div>
          <div className="text-xs text-gray-600">3 models combined</div>
        </div>
      </div>
    </header>
  );
};

export default Header;
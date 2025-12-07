import React, { useState } from 'react';

const StockSelector = ({
  stocks,
  selectedSymbol,
  isValidSymbol,
  validationMessage,
  onStockSelect,
  onValidateStock,
  onPredict,
  isLoading
}) => {
  const [searchInput, setSearchInput] = useState('');

  const handleDropdownChange = (e) => {
    const symbol = e.target.value;
    if (symbol) {
      onStockSelect(symbol);
      setSearchInput('');
    }
  };

  const handleSearchClick = () => {
    if (searchInput.trim()) {
      onValidateStock(searchInput.trim());
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearchClick();
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">
        Select or Search Stock
      </h2>

      {/* Popular Stocks Dropdown */}
      <div>
        <label className="block text-gray-700 font-semibold mb-2">
          Popular Stocks:
        </label>
        <select
          onChange={handleDropdownChange}
          value={selectedSymbol}
          className="w-full px-4 py-3 text-lg border-2 border-gray-300 rounded-xl focus:outline-none focus:border-primary-500 transition-colors bg-white cursor-pointer hover:border-primary-400"
        >
          <option value="">-- Choose a Stock --</option>
          {stocks.map((stock) => (
            <option key={stock} value={stock}>
              {stock}
            </option>
          ))}
        </select>
      </div>

      {/* OR Divider */}
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t-2 border-gray-300"></div>
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="px-4 bg-white text-gray-500 font-bold text-lg">OR</span>
        </div>
      </div>

      {/* Custom Search */}
      <div>
        <label className="block text-gray-700 font-semibold mb-2">
          Search Stock Symbol:
        </label>
        <div className="flex gap-3">
          <input
            type="text"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value.toUpperCase())}
            onKeyPress={handleKeyPress}
            placeholder="e.g., AAPL, TSLA, MSFT"
            className="flex-1 px-4 py-3 text-lg border-2 border-gray-300 rounded-xl focus:outline-none focus:border-primary-500 transition-colors"
          />
          <button
            onClick={handleSearchClick}
            disabled={isLoading || !searchInput.trim()}
            className="px-6 py-3 bg-primary-500 text-white font-semibold rounded-xl hover:bg-primary-600 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            Search
          </button>
        </div>
        <small className="text-gray-500 mt-2 block">
          Enter stock ticker symbol and click Search to verify availability
        </small>
      </div>

      {/* Selected Stock Display */}
      {selectedSymbol && (
        <div className={`p-4 rounded-xl border-2 ${
          isValidSymbol 
            ? 'bg-blue-50 border-primary-500' 
            : 'bg-red-50 border-red-500'
        }`}>
          <div className="flex justify-between items-center">
            <span className="text-xl font-bold text-gray-800">
              {selectedSymbol}
            </span>
            <span className={`px-4 py-1 rounded-full text-sm font-semibold ${
              isValidSymbol
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800'
            }`}>
              {validationMessage}
            </span>
          </div>
        </div>
      )}

      {/* Predict Button */}
      <button
        onClick={onPredict}
        disabled={!isValidSymbol || isLoading}
        className="w-full py-4 bg-gradient-primary text-white text-xl font-bold rounded-xl hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300 disabled:bg-gray-400 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-none"
      >
        {isLoading ? (
          <span className="flex items-center justify-center">
            <svg className="animate-spin h-6 w-6 mr-3" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Processing...
          </span>
        ) : (
          '🔮 Predict Next 7 Days'
        )}
      </button>
    </div>
  );
};

export default StockSelector;
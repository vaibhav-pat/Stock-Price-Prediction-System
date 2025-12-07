import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="relative">
        <div className="w-20 h-20 border-8 border-gray-200 border-t-primary-500 rounded-full animate-spin"></div>
      </div>
      <p className="mt-6 text-gray-700 text-lg font-medium text-center">
        Analyzing stock data and training models...
        <br />
        <span className="text-gray-500 text-base">This may take 30-60 seconds</span>
      </p>
    </div>
  );
};

export default LoadingSpinner;
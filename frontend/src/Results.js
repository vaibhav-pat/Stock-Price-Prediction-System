import React from 'react';
import PredictionChart from './PredictionChart';

const Results = ({ predictions }) => {
  const { symbol, current_high, current_low, predictions: predData } = predictions;

  return (
    <div className="mt-8 space-y-6">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">
        📈 Prediction Results
      </h2>

      {/* Current Price Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gradient-primary text-white p-6 rounded-2xl shadow-lg">
          <div className="text-sm opacity-90 mb-2">Current High</div>
          <div className="text-4xl font-bold">${current_high}</div>
        </div>
        <div className="bg-gradient-primary text-white p-6 rounded-2xl shadow-lg">
          <div className="text-sm opacity-90 mb-2">Current Low</div>
          <div className="text-4xl font-bold">${current_low}</div>
        </div>
      </div>

      {/* Chart */}
      <div className="bg-gray-50 p-6 rounded-2xl">
        <PredictionChart symbol={symbol} predictions={predData} />
      </div>

      {/* Predictions Table */}
      <div className="overflow-x-auto rounded-2xl shadow-lg">
        <table className="w-full bg-white">
          <thead className="bg-gradient-primary text-white">
            <tr>
              <th className="px-6 py-4 text-left font-semibold">Day</th>
              <th className="px-6 py-4 text-left font-semibold">Predicted High ($)</th>
              <th className="px-6 py-4 text-left font-semibold">Predicted Low ($)</th>
              <th className="px-6 py-4 text-left font-semibold">Range ($)</th>
            </tr>
          </thead>
          <tbody>
            {predData.map((pred, index) => {
              const range = (pred.high - pred.low).toFixed(2);
              return (
                <tr
                  key={pred.day}
                  className={`border-b hover:bg-gray-50 transition-colors ${
                    index % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                  }`}
                >
                  <td className="px-6 py-4 font-semibold text-gray-800">
                    Day {pred.day}
                  </td>
                  <td className="px-6 py-4 text-gray-700 font-medium">
                    ${pred.high}
                  </td>
                  <td className="px-6 py-4 text-gray-700 font-medium">
                    ${pred.low}
                  </td>
                  <td className="px-6 py-4 text-gray-600">
                    ${range}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Disclaimer */}
      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-lg">
        <div className="flex items-start">
          <div className="text-yellow-600 text-2xl mr-3">⚠️</div>
          <div>
            <p className="font-bold text-yellow-800 mb-1">Disclaimer</p>
            <p className="text-yellow-700 text-sm">
              These predictions are for educational purposes only. Always consult 
              financial advisors before making investment decisions. Past performance 
              does not guarantee future results.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;
import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const PredictionChart = ({ symbol, predictions }) => {
  const days = predictions.map((p) => `Day ${p.day}`);
  const highPrices = predictions.map((p) => p.high);
  const lowPrices = predictions.map((p) => p.low);

  const data = {
    labels: days,
    datasets: [
      {
        label: 'Predicted High Price',
        data: highPrices,
        borderColor: '#667eea',
        backgroundColor: 'rgba(102, 126, 234, 0.1)',
        borderWidth: 3,
        fill: false,
        tension: 0.4,
        pointRadius: 6,
        pointHoverRadius: 8,
        pointBackgroundColor: '#667eea',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
      },
      {
        label: 'Predicted Low Price',
        data: lowPrices,
        borderColor: '#764ba2',
        backgroundColor: 'rgba(118, 75, 162, 0.1)',
        borderWidth: 3,
        fill: false,
        tension: 0.4,
        pointRadius: 6,
        pointHoverRadius: 8,
        pointBackgroundColor: '#764ba2',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      title: {
        display: true,
        text: `${symbol} - 7 Day Price Prediction`,
        font: {
          size: 20,
          weight: 'bold',
        },
        color: '#1f2937',
      },
      legend: {
        display: true,
        position: 'top',
        labels: {
          font: {
            size: 14,
          },
          color: '#4b5563',
          padding: 15,
        },
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleFont: {
          size: 14,
        },
        bodyFont: {
          size: 13,
        },
        padding: 12,
        callbacks: {
          label: function (context) {
            return context.dataset.label + ': $' + context.parsed.y.toFixed(2);
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: false,
        ticks: {
          callback: function (value) {
            return '$' + value.toFixed(2);
          },
          font: {
            size: 12,
          },
          color: '#6b7280',
        },
        title: {
          display: true,
          text: 'Price ($)',
          font: {
            size: 14,
            weight: 'bold',
          },
          color: '#374151',
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Prediction Timeline',
          font: {
            size: 14,
            weight: 'bold',
          },
          color: '#374151',
        },
        ticks: {
          font: {
            size: 12,
          },
          color: '#6b7280',
        },
        grid: {
          display: false,
        },
      },
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false,
    },
  };

  return (
    <div className="p-4">
      <Line data={data} options={options} />
    </div>
  );
};

export default PredictionChart;
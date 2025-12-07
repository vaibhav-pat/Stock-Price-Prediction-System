let selectedSymbol = '';
let predictionChart = null;

// Select stock from dropdown
function selectStock() {
    const select = document.getElementById('stockSelect');
    const symbol = select.value;
    
    if (symbol) {
        selectedSymbol = symbol;
        document.getElementById('stockSearch').value = '';
        showSelectedStock(symbol, true, 'Stock selected');
        document.getElementById('predictBtn').disabled = false;
    } else {
        hideSelectedStock();
        document.getElementById('predictBtn').disabled = true;
    }
}

// Search stock on Enter key
function searchStock(event) {
    if (event.key === 'Enter') {
        validateSearch();
    }
}

// Validate searched stock
async function validateSearch() {
    const input = document.getElementById('stockSearch');
    const symbol = input.value.trim().toUpperCase();
    
    if (!symbol) {
        alert('Please enter a stock symbol');
        return;
    }
    
    // Show loading
    showSelectedStock(symbol, false, 'Validating...');
    
    try {
        const response = await fetch('/search_stock', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol: symbol })
        });
        
        const data = await response.json();
        
        if (data.success) {
            selectedSymbol = symbol;
            document.getElementById('stockSelect').value = '';
            showSelectedStock(symbol, true, data.message);
            document.getElementById('predictBtn').disabled = false;
        } else {
            showSelectedStock(symbol, false, data.message);
            document.getElementById('predictBtn').disabled = true;
        }
        
    } catch (error) {
        showSelectedStock(symbol, false, 'Error validating stock');
        document.getElementById('predictBtn').disabled = true;
    }
}

// Show selected stock
function showSelectedStock(symbol, isValid, message) {
    const container = document.getElementById('selectedStock');
    const symbolEl = document.getElementById('displaySymbol');
    const badge = document.getElementById('statusBadge');
    
    symbolEl.textContent = symbol;
    badge.textContent = message;
    badge.className = 'status-badge ' + (isValid ? 'valid' : 'invalid');
    
    container.style.display = 'block';
}

// Hide selected stock
function hideSelectedStock() {
    document.getElementById('selectedStock').style.display = 'none';
    selectedSymbol = '';
}

// Predict stock prices
async function predictStock() {
    if (!selectedSymbol) {
        alert('Please select a stock first');
        return;
    }
    
    // Hide results and show loading
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('loadingSpinner').style.display = 'block';
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol: selectedSymbol })
        });
        
        const data = await response.json();
        
        // Hide loading
        document.getElementById('loadingSpinner').style.display = 'none';
        
        if (data.success) {
            displayResults(data);
        } else {
            alert('Prediction failed: ' + data.message);
        }
        
    } catch (error) {
        document.getElementById('loadingSpinner').style.display = 'none';
        alert('Error: ' + error.message);
    }
}

// Display prediction results
function displayResults(data) {
    // Show results section
    document.getElementById('resultsSection').style.display = 'block';
    
    // Update current prices
    document.getElementById('currentHigh').textContent = '$' + data.current_high;
    document.getElementById('currentLow').textContent = '$' + data.current_low;
    
    // Update table
    const tbody = document.getElementById('predictionsBody');
    tbody.innerHTML = '';
    
    data.predictions.forEach(function(pred) {
        const range = (pred.high - pred.low).toFixed(2);
        const row = '<tr>' +
            '<td>Day ' + pred.day + '</td>' +
            '<td>$' + pred.high + '</td>' +
            '<td>$' + pred.low + '</td>' +
            '<td>$' + range + '</td>' +
            '</tr>';
        tbody.innerHTML += row;
    });
    
    // Create chart
    createChart(data);
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

// Create prediction chart
function createChart(data) {
    const ctx = document.getElementById('predictionChart').getContext('2d');
    
    // Destroy existing chart if any
    if (predictionChart) {
        predictionChart.destroy();
    }
    
    const days = data.predictions.map(function(p) { return 'Day ' + p.day; });
    const highPrices = data.predictions.map(function(p) { return p.high; });
    const lowPrices = data.predictions.map(function(p) { return p.low; });
    
    predictionChart = new Chart(ctx, {
        type: 'line',
        data: {
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
                    pointRadius: 5,
                    pointHoverRadius: 7
                },
                {
                    label: 'Predicted Low Price',
                    data: lowPrices,
                    borderColor: '#764ba2',
                    backgroundColor: 'rgba(118, 75, 162, 0.1)',
                    borderWidth: 3,
                    fill: false,
                    tension: 0.4,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: data.symbol + ' - 7 Day Price Prediction',
                    font: {
                        size: 18,
                        weight: 'bold'
                    }
                },
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': $' + context.parsed.y.toFixed(2);
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    },
                    title: {
                        display: true,
                        text: 'Price ($)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Prediction Timeline'
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}
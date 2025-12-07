# Stock-Price-Prediction-System

A simple stock price prediction web app that uses multiple models (ARIMA, LSTM, Prophet) and an ensemble to predict the next 7 days' high and low prices for a chosen stock.

This README explains, in simple manual language, how to set up and run the project on your machine.

## What this project does
- Fetches historical stock data (Alpha Vantage by default).
- Preprocesses the data and runs three prediction models (ARIMA, LSTM, Prophet).
- Combines model outputs into a final prediction (ensemble).
- Provides a web interface to pick a stock and view current price + 7-day predictions.

## Quick requirements
- Python 3.10+ and `pip` installed.
- Node.js and `npm` (for the frontend) if you want the React UI.
- An Alpha Vantage API key (free) for reliable data access.

## Python dependencies
Install the Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Frontend dependencies
If you want to run the React frontend, go to the `frontend` folder and install npm packages:

```bash
cd frontend
npm install
```

## Setting the Alpha Vantage API key
- Open `utils/data_fetcher_alphavantage.py`.
- Set your API key in the `API_KEY` variable near the top of the file.
- You can get a free key from: https://www.alphavantage.co/support/#api-key

Note: The app will warn you if no API key is configured.

## Run the backend (Flask)
From the project root run:

```bash
python app.py
```

This starts a server at `http://localhost:5000` by default.

## Run the frontend (optional)
From the `frontend` folder run:

```bash
npm start
```

The frontend will usually run on `http://localhost:3000` and talk to the backend at port `5000`.

## How to use the app
1. Start the backend (`python app.py`).
2. (Optional) Start the frontend (`cd frontend && npm start`).
3. Open your browser and go to `http://localhost:5000` (or the frontend address).
4. Pick or search a stock ticker (for example, `AAPL`) and click Predict.
5. The page will show the current high/low and predicted highs/lows for the next 7 days.

## Project layout (short)
- `app.py` – Flask backend and API endpoints.
- `frontend/` – React UI (optional).
- `models/` – Prediction model implementations (`arima_model.py`, `lstm_model.py`, `prophet_model.py`, `ensemble.py`).
- `utils/` – Data fetchers and preprocessing.
- `templates/`, `static/` – Frontend served by Flask (if not using React dev server).

## Notes & troubleshooting
- Alpha Vantage free tier has rate limits (5 calls per minute). If you hit the limit the code sleeps and retries once.
- If you see "Insufficient data" errors, try another ticker or use `outputsize='full'` (already default).
- If models are slow on your machine, you can skip the LSTM by modifying the code, or run without the frontend.

## Contributing
- Feel free to open issues or submit pull requests. Small, focused changes are easiest to review.

## License
This repository has no license file. Add one if you plan to share publicly.

---

If you'd like, I can also: run the app locally, start the frontend, or add a short usage GIF to the README. Which would you like next?

# 📈 Stock Research Agent

An interactive Streamlit app for analyzing stocks, generating BUY/SELL signals, and visualizing key indicators.

## 🚀 Features
- Dynamic stock symbol input
- Candlestick chart with SMA20 and SMA50
- RSI and MACD plots (side-by-side view)
- Buy/Sell signals with markers on charts
- Backtest table of signal dates + indicator values
- Runs in the cloud via Streamlit

## 📊 Indicators used
- **Simple Moving Averages (SMA 20 / 50)**
- **Relative Strength Index (RSI)** — with overbought/oversold thresholds
- **MACD / Signal line**

## 💡 How to use
1️⃣ Enter a stock symbol in the input box (e.g. `AAPL`, `TSLA`)  
2️⃣ Click `Add Stock`  
3️⃣ Check `Run backtest + plot signals` for each stock  
4️⃣ View charts, markers, and signal tables

## 🌐 Live App
👉 [Click here to open](YOUR_STREAMLIT_APP_URL)

## ⚙️ Requirements
streamlit
yfinance
pandas
plotly

## 📌 How to run locally
```bash
git clone https://github.com/ypratap11/stock_research_agent_py.git
cd stock_research_agent_py
pip install -r requirements.txt
streamlit run app.py

Coming:

Profit tracking after signals

CSV export of signals

Email / Telegram alerts

Cloud deployment enhancements

Stop loss / take profit logic

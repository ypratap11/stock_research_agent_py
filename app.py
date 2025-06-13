import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def fetch_data(ticker):
    return yf.Ticker(ticker).history(period="6mo")

def calculate_indicators(df):
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    return df

def backtest_signals(df):
    buy_signals = []
    sell_signals = []
    for i in range(50, len(df)):
        rsi = df['RSI'].iloc[i]
        macd = df['MACD'].iloc[i]
        signal = df['Signal'].iloc[i]
        close = df['Close'].iloc[i]
        sma20 = df['SMA20'].iloc[i]

        if rsi < 35 and macd > signal and close > sma20:
            buy_signals.append({'Date': df.index[i], 'Close': close, 'RSI': rsi, 'MACD': macd})
        if rsi > 65 and macd < signal:
            sell_signals.append({'Date': df.index[i], 'Close': close, 'RSI': rsi, 'MACD': macd})
    return buy_signals, sell_signals

def plot_main_chart(df, buy_signals, sell_signals):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name="Candlestick"))
    fig.add_trace(go.Scatter(
        x=df.index, y=df['SMA20'], line=dict(color='blue', width=1), name="SMA 20"))
    fig.add_trace(go.Scatter(
        x=df.index, y=df['SMA50'], line=dict(color='orange', width=1), name="SMA 50"))

    if buy_signals:
        fig.add_trace(go.Scatter(
            x=[s['Date'] for s in buy_signals],
            y=[s['Close'] for s in buy_signals],
            mode="markers", marker=dict(symbol="arrow-up", color="green", size=14),
            name="Buy Signal"))
    if sell_signals:
        fig.add_trace(go.Scatter(
            x=[s['Date'] for s in sell_signals],
            y=[s['Close'] for s in sell_signals],
            mode="markers", marker=dict(symbol="arrow-down", color="red", size=14),
            name="Sell Signal"))
    st.plotly_chart(fig, use_container_width=True)

def plot_rsi_macd(df, buy_signals, sell_signals):
    col1, col2 = st.columns(2)

    with col1:
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=df.index, y=df['RSI'], line=dict(color='purple'), name="RSI"))
        if buy_signals:
            fig_rsi.add_trace(go.Scatter(
                x=[s['Date'] for s in buy_signals], y=[s['RSI'] for s in buy_signals],
                mode="markers", marker=dict(color="green", size=10), name="Buy"))
        if sell_signals:
            fig_rsi.add_trace(go.Scatter(
                x=[s['Date'] for s in sell_signals], y=[s['RSI'] for s in sell_signals],
                mode="markers", marker=dict(color="red", size=10), name="Sell"))
        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
        fig_rsi.update_layout(title="RSI")
        st.plotly_chart(fig_rsi, use_container_width=True)

    with col2:
        fig_macd = go.Figure()
        fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD'], line=dict(color='teal'), name="MACD"))
        fig_macd.add_trace(go.Scatter(x=df.index, y=df['Signal'], line=dict(color='orange'), name="Signal"))
        if buy_signals:
            fig_macd.add_trace(go.Scatter(
                x=[s['Date'] for s in buy_signals], y=[s['MACD'] for s in buy_signals],
                mode="markers", marker=dict(color="green", size=10), name="Buy"))
        if sell_signals:
            fig_macd.add_trace(go.Scatter(
                x=[s['Date'] for s in sell_signals], y=[s['MACD'] for s in sell_signals],
                mode="markers", marker=dict(color="red", size=10), name="Sell"))
        fig_macd.update_layout(title="MACD")
        st.plotly_chart(fig_macd, use_container_width=True)

# Streamlit app
st.title("📊 Dynamic Stock Research Agent")

# Initialize dynamic watchlist
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ["AAPL", "TSLA"]

new_stock = st.text_input("Add a stock symbol (e.g., MSFT)")
if st.button("Add Stock"):
    if new_stock.strip() != "":
        st.session_state.watchlist.append(new_stock.strip().upper())

st.write("📌 **Current Watchlist:**", ", ".join(st.session_state.watchlist))

for ticker in st.session_state.watchlist:
    st.header(f"📈 {ticker}")
    df = fetch_data(ticker)
    if df.empty:
        st.warning(f"No data found for {ticker}")
        continue

    df = calculate_indicators(df)

    buy_signals, sell_signals = [], []
    if st.checkbox(f"Run backtest + plot signals for {ticker}"):
        buy_signals, sell_signals = backtest_signals(df)
        st.write(f"✅ {len(buy_signals)} Buy Signals | ⚠️ {len(sell_signals)} Sell Signals")
        st.dataframe(pd.DataFrame({
            'Date': [s['Date'].strftime('%Y-%m-%d') for s in buy_signals],
            'Close': [round(s['Close'], 2) for s in buy_signals],
            'RSI': [round(s['RSI'], 1) for s in buy_signals],
            'MACD': [round(s['MACD'], 2) for s in buy_signals]
        }), height=200)
        st.dataframe(pd.DataFrame({
            'Date': [s['Date'].strftime('%Y-%m-%d') for s in sell_signals],
            'Close': [round(s['Close'], 2) for s in sell_signals],
            'RSI': [round(s['RSI'], 1) for s in sell_signals],
            'MACD': [round(s['MACD'], 2) for s in sell_signals]
        }), height=200)

    plot_main_chart(df, buy_signals, sell_signals)
    plot_rsi_macd(df, buy_signals, sell_signals)

import yfinance as yf
import streamlit as st
import pandas as pd

st.set_page_config(page_title="📈 Stock Price App", layout="centered")

st.write("""
# 📈 Stock Price App
This app retrieves stock prices for a given ticker symbol using Yahoo Finance.
""")

# Inputs
ticker_symbol = st.text_input("Enter Stock Ticker Symbol", "AAPL")
start = st.date_input("Start Date", pd.to_datetime("2025-01-01"))
end = st.date_input("End Date", pd.to_datetime("2025-07-01"))

# Cache the API call to avoid repeated requests
@st.cache_data(show_spinner=True)
def load_data(ticker, start, end):
    try:
        ticker_data = yf.Ticker(ticker)
        df = ticker_data.history(start=start, end=end, interval="1wk")  # '1wk' reduces API load
        if df.empty:
            raise ValueError("No data found. Check your ticker or date range.")
        return df
    except Exception as e:
        if "rate limit" in str(e).lower():
            st.error("⚠️ Rate limited by Yahoo Finance. Please wait a few minutes and try again.")
        else:
            st.error(f"❌ An error occurred: {e}")
        return None

# Show charts only when button is clicked
if st.button("Get Stock Data"):
    df = load_data(ticker_symbol, start, end)
    if df is not None:
        st.subheader("📊 Closing Price")
        st.line_chart(df.Close)

        st.subheader("🔊 Volume Traded")
        st.line_chart(df.Volume)
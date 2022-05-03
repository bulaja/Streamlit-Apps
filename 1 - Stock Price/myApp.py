import yfinance as yf
import streamlit as st
import pandas as pd


# TIcker freeform entry - Default Apple
tickerSymbol = st.sidebar.text_input("Enter Ticker", value="AAPL")

# Options for period, select one
options = [ "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
chosenPeriod = st.sidebar.selectbox("Select period", options, index = 5)


# Get data of the chosen ticker
tickerData = yf.Ticker(tickerSymbol)

# Get the company name
company_name = tickerData.info['longName']

# Text to write on top
st.write(f"""
# My Super Cool Stock Price App

Shown are the stock **closing price** and **volume** of
***{company_name}***
"""
)

# Get the historical prices for this ticker
tickerDf = tickerData.history(period = chosenPeriod)

# Closing Price graph
st.write("""
## Closing Price
"""
)
st.line_chart(tickerDf.Close)

# Volume graph
st.write("""
## Volume
"""
)
st.line_chart(tickerDf.Volume)
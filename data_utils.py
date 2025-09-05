# 📄 data_utils.py

"""Handles all data fetching from yfinance and other external APIs."""

import streamlit as st
import yfinance as yf
import requests

@st.cache_data
def search_for_ticker(query: str):
    """Searches for a stock ticker using Yahoo Finance's public API."""
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("quotes", [])
    except requests.exceptions.RequestException as e:
        st.toast(f"Network error during search: {e}", icon="🌐")
        return []
    except (KeyError, IndexError, requests.exceptions.JSONDecodeError):
        st.toast("Could not parse search results.", icon="⚠️")
        return []

@st.cache_data
def get_stock_data(ticker, start_date, end_date):
    """Retrieves and validates stock info and historical data."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if not info or ('longName' not in info and 'shortName' not in info):
            return None, None
        historical_data = stock.history(start=start_date, end=end_date)
        if historical_data.empty:
            return info, None
        return info, historical_data
    except Exception:
        return None, None

@st.cache_data
def get_stock_info(ticker):
    """Retrieves just the info dictionary for a ticker, optimized for comparison."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info if info and 'shortName' in info else None
    except Exception:
        return None

@st.cache_data
def get_exchange_rate(from_currency, to_currency):
    """Fetches the currency exchange rate from Yahoo Finance."""
    if from_currency == to_currency: return 1.0
    try:
        data = yf.Ticker(f"{from_currency}{to_currency}=X")
        rate = data.info.get("regularMarketPrice")
        return float(rate) if rate else None
    except Exception: return None
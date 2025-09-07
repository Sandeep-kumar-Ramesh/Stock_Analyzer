import streamlit as st
import yfinance as yf
import requests
from requests.exceptions import RequestException, JSONDecodeError

@st.cache_data
def search_for_ticker(query: str):
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("quotes", [])
    except RequestException as e:
        st.toast(f"Network error during search: {e}", icon="🌐")
        return []
    except (KeyError, IndexError, JSONDecodeError):
        st.toast("Could not parse search results.", icon="⚠️")
        return []

@st.cache_data
def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if info and ('shortName' in info or 'longName' in info):
            return info
        return None
    except Exception:
        return None

@st.cache_data
def get_stock_data(ticker, start_date, end_date):
    info = get_stock_info(ticker)
    if not info:
        return None, None
    
    try:
        stock = yf.Ticker(ticker)
        historical_data = stock.history(start=start_date, end=end_date)
        if historical_data.empty:
            return info, None
        return info, historical_data
    except Exception:
        return info, None

@st.cache_data
def get_exchange_rate(from_currency, to_currency):
    if from_currency == to_currency:
        return 1.0
    try:
        data = yf.Ticker(f"{from_currency}{to_currency}=X")   # e.g., USDEUR=X
        rate = data.info.get("regularMarketPrice")
        return float(rate) if rate else None
    except (TypeError, ValueError, AttributeError):
        return None

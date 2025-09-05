# 📄 ui_components.py

"""Module for creating reusable Streamlit UI components."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta
from typing import Dict, Any

from constants import FINANCIAL_METRICS
from data_utils import search_for_ticker

# --- UI Helper and Callback Functions ---
def set_date_range(days: int, label: str):
    """Callback to set dates and show a toast."""
    st.session_state.end_date = date.today()
    st.session_state.start_date = date.today() - timedelta(days=days)
    st.toast(f"Date range set to the last {label}.", icon="🗓️")

def reset_dates():
    """Callback to reset dates to 1 year."""
    set_date_range(365, "year")

def format_metric_value(value: Any, metric_name: str = "", currency_symbol: str = "$", rate: float = 1.0) -> str:
    """Formats a financial metric value based on its type (currency, percentage, etc.)."""
    if not isinstance(value, (int, float)):
        return "N/A"

    if any(sub in metric_name for sub in ["Yield", "Margins", "ROE", "Payout", "Growth"]):
        return f"{value * 100:.2f}%"

    if any(sub in metric_name for sub in ["Cap", "Value", "Cash", "Debt", "EBITDA"]):
        value *= (rate or 1.0)
        if abs(value) >= 1_000_000_000_000: return f"{currency_symbol}{value / 1_000_000_000_000:.2f}T"
        if abs(value) >= 1_000_000_000: return f"{currency_symbol}{value / 1_000_000_000:.2f}B"
        if abs(value) >= 1_000_000: return f"{currency_symbol}{value / 1_000_000:.2f}M"
    
    return f"{value:,.2f}"

# --- Major UI Components ---
def display_financial_metrics(info: Dict[str, Any], exchange_rate: float, currency_symbol: str):
    """Displays key financial metrics in a styled dataframe."""
    if not info:
        st.warning("Financial information not available for this stock.")
        return
    
    data = []
    for display_name, key in FINANCIAL_METRICS.items():
        if key is None:
            data.append({"Metric": f"**{display_name}**", "Value": ''})
            continue
        value = info.get(key)
        formatted_value = format_metric_value(value, display_name, currency_symbol, exchange_rate)
        data.append({"Metric": display_name, "Value": formatted_value})

    df = pd.DataFrame(data)

    def style_headers(row):
        return ['font-weight: bold; color: #0078D4; text-align: left; font-size: 1.1em;', ''] if str(row['Metric']).startswith('**') else ['', '']
            
    styler = df.style.apply(style_headers, axis=1)
    with st.expander("Key Financial Metrics", expanded=True):
        st.dataframe(styler, use_container_width=True, hide_index=True)

def create_price_chart(historical_data: pd.DataFrame, ticker: str, exchange_rate: float, currency_symbol: str, chart_type: str):
    """Creates and displays a Plotly price chart."""
    df_converted = historical_data.copy()
    rate = exchange_rate or 1.0
    for col in ['Open', 'High', 'Low', 'Close']: df_converted[col] *= rate
    
    fig = go.Figure()
    if chart_type == "Candlestick": fig.add_trace(go.Candlestick(x=df_converted.index, open=df_converted['Open'], high=df_converted['High'], low=df_converted['Low'], close=df_converted['Close'], name='Candlestick'))
    elif chart_type == "Line": fig.add_trace(go.Scatter(x=df_converted.index, y=df_converted['Close'], mode='lines', name='Close Price', line=dict(color='#17BECF', width=2)))
    elif chart_type == "Area": fig.add_trace(go.Scatter(x=df_converted.index, y=df_converted['Close'], mode='lines', fill='tozeroy', name='Price Area', line=dict(color='#636EFA')))
    elif chart_type == "Line with Moving Averages":
        df_converted['MA50'] = df_converted['Close'].rolling(window=50).mean()
        df_converted['MA200'] = df_converted['Close'].rolling(window=200).mean()
        fig.add_trace(go.Scatter(x=df_converted.index, y=df_converted['Close'], mode='lines', name='Close Price', line=dict(color='#17BECF', width=2)))
        fig.add_trace(go.Scatter(x=df_converted.index, y=df_converted['MA50'], mode='lines', name='50-Day MA', line=dict(color='orange', width=1.5, dash='dot')))
        fig.add_trace(go.Scatter(x=df_converted.index, y=df_converted['MA200'], mode='lines', name='200-Day MA', line=dict(color='magenta', width=1.5, dash='dot')))
    
    fig.update_layout(
        title=f"Historical Price Performance of {ticker} ({chart_type})", yaxis_title=f"Stock Price ({currency_symbol})", 
        template="plotly_dark", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

def company_search_box(label: str, key_prefix: str):
    """Creates a company search box that returns a selected ticker."""
    st.markdown(f"**{label}**")
    company_name = st.text_input(
        "Enter company name:", 
        key=f"{key_prefix}_name", 
        placeholder="e.g., Apple",
        help="Type a name and press Enter to search."
    )
    selected_ticker = None
    if company_name:
        with st.spinner("Searching..."): 
            search_results = search_for_ticker(company_name)
        
        if search_results:
            ticker_options = {f"{res.get('longname', res.get('shortname', 'N/A'))} ({res['symbol']})": res['symbol'] 
                for res in search_results if 'symbol' in res and res.get('quoteType') == 'EQUITY'}
            if ticker_options:
                selected_option = st.selectbox("Select the correct company:", options=list(ticker_options.keys()), key=f"{key_prefix}_select")
                selected_ticker = ticker_options[selected_option]
            else:
                st.info("No valid stock tickers found for your query. Please try a different name.", icon="ℹ️")
        elif company_name:
            st.error("Search failed or returned no results. Please check your query or network connection.", icon="❌")
            
    return selected_ticker

def create_comparison_table(info1, info2, ticker1, ticker2):
    """Creates a side-by-side comparison table with highlighting."""
    raw_data, display_data = [], []
    
    for display_name, key in FINANCIAL_METRICS.items():
        if key is None:
            raw_data.append({"Metric": f"**{display_name}**", ticker1: None, ticker2: None})
            display_data.append({"Metric": f"**{display_name}**", ticker1: '', ticker2: ''})
            continue
        val1, val2 = info1.get(key), info2.get(key)
        raw_data.append({"Metric": display_name, ticker1: val1, ticker2: val2})
        display_data.append({
            "Metric": display_name, 
            ticker1: format_metric_value(val1, display_name), 
            ticker2: format_metric_value(val2, display_name)
        })

    df_raw, df_display = pd.DataFrame(raw_data), pd.DataFrame(display_data)
    df_raw.set_index('Metric', inplace=True); df_display.set_index('Metric', inplace=True)
    
    def highlight_better(row):
        metric_name, styles = row.name, [''] * len(row)
        if metric_name.startswith('**'): return styles
        raw_values = df_raw.loc[metric_name]
        val1, val2 = raw_values[ticker1], raw_values[ticker2]
        if not isinstance(val1, (int, float)) or not isinstance(val2, (int, float)): return styles
        lower_is_better = ["Trailing P/E", "Forward P/E", "PEG Ratio", "Price/Book (P/B)", "EV/Revenue", "EV/EBITDA", "Debt/Equity", "Payout Ratio"]
        winner_style = 'background-color: #1A3C34; color: #A7D7C5;'
        idx1, idx2 = row.index.get_loc(ticker1), row.index.get_loc(ticker2)
        if (metric_name in lower_is_better and val1 < val2) or (metric_name not in lower_is_better and val1 > val2): styles[idx1] = winner_style
        elif (metric_name in lower_is_better and val2 < val1) or (metric_name not in lower_is_better and val2 > val1): styles[idx2] = winner_style
        return styles
    
    styler = df_display.style.apply(highlight_better, axis=1)
    st.dataframe(styler, use_container_width=True)
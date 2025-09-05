"""Module for creating reusable Streamlit UI components."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta
from typing import Dict, Any

from constants import FINANCIAL_METRICS, CURRENCY_SYMBOLS
from data_utils import search_for_ticker

# --- UI Helper and Callback Functions ---
def _set_date_range(days: int, label: str):
    """Callback to set dates and queue a toast message."""
    st.session_state.end_date = date.today()
    st.session_state.start_date = date.today() - timedelta(days=days)
    # FIX: Queue a message instead of calling toast directly
    st.session_state.toast_message = f"Date range set to the last {label}."

def _reset_dates():
    """Callback to reset dates to 1 year."""
    _set_date_range(365, "year")

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

# --- Reusable UI Sections ---

def render_date_range_buttons():
    """Renders the date range shortcut buttons in the sidebar."""
    col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
    with col1: st.button("Reset", on_click=_reset_dates, use_container_width=True)
    with col2: st.button("1M", on_click=_set_date_range, args=(30, "month"), use_container_width=True)
    with col3: st.button("3M", on_click=_set_date_range, args=(90, "3 months"), use_container_width=True)
    with col4: st.button("6M", on_click=_set_date_range, args=(180, "6 months"), use_container_width=True)

def render_currency_converter(stock_currency: str):
    """Renders the currency selection box."""
    currency_options = list(CURRENCY_SYMBOLS.keys())
    try:
        default_index = currency_options.index(stock_currency)
    except ValueError:
        default_index = 0
    
    st.selectbox(
        "Display currency:",
        currency_options,
        index=default_index,
        key="selected_currency" # Use this key to track changes
    )

# --- The rest of the file (from create_price_chart onwards) remains the same as your last version ---
def display_financial_metrics(info: Dict[str, Any], exchange_rate: float, currency_symbol: str):
    """Displays key financial metrics in a styled dataframe."""
    data = []
    for display_name, key in FINANCIAL_METRICS.items():
        if key is None:
            data.append({"Metric": f"**{display_name}**", "Value": ''})
            continue
        value = info.get(key)
        formatted_value = format_metric_value(value, display_name, currency_symbol, exchange_rate)
        data.append({"Metric": display_name, "Value": formatted_value})

    df = pd.DataFrame(data)
    styler = df.style.apply(
        lambda row: ['font-weight: bold; color: #0078D4; text-align: left; font-size: 1.1em;', ''] if str(row['Metric']).startswith('**') else ['', ''],
        axis=1
    )
    with st.expander("Key Financial Metrics", expanded=True):
        st.dataframe(styler, use_container_width=True, hide_index=True)

def create_price_chart(historical_data: pd.DataFrame, ticker: str, exchange_rate: float, currency_symbol: str, chart_type: str):
    """Creates and displays a Plotly price chart."""
    df_converted = historical_data.copy()
    rate = exchange_rate or 1.0
    for col in ['Open', 'High', 'Low', 'Close']:
        df_converted[col] *= rate
    
    fig = go.Figure()
    if chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(x=df_converted.index, open=df_converted['Open'], high=df_converted['High'], low=df_converted['Low'], close=df_converted['Close'], name='Candlestick'))
    elif chart_type == "Line":
        fig.add_trace(go.Scatter(x=df_converted.index, y=df_converted['Close'], mode='lines', name='Close Price', line=dict(color='#17BECF', width=2)))
    elif chart_type == "Area":
        fig.add_trace(go.Scatter(x=df_converted.index, y=df_converted['Close'], mode='lines', fill='tozeroy', name='Price Area', line=dict(color='#636EFA')))
    elif chart_type == "Line with Moving Averages":
        df_converted['MA50'] = df_converted['Close'].rolling(window=50).mean()
        df_converted['MA200'] = df_converted['Close'].rolling(window=200).mean()
        fig.add_trace(go.Scatter(x=df_converted.index, y=df_converted['Close'], mode='lines', name='Close Price', line=dict(color='#17BECF', width=2)))
        fig.add_trace(go.Scatter(x=df_converted.index, y=df_converted['MA50'], mode='lines', name='50-Day MA', line=dict(color='orange', width=1.5, dash='dot')))
        fig.add_trace(go.Scatter(x=df_converted.index, y=df_converted['MA200'], mode='lines', name='200-Day MA', line=dict(color='magenta', width=1.5, dash='dot')))
    
    fig.update_layout(
        title=f"Historical Price Performance of {ticker} ({chart_type})",
        yaxis_title=f"Stock Price ({currency_symbol})",
        template="plotly_dark",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig, use_container_width=True)

def company_search_box(label: str, key_prefix: str) -> str | None:
    """Creates a company search box that returns a selected ticker."""
    company_name = st.text_input(
        "Enter company name or ticker:",
        key=f"{key_prefix}_name",
        placeholder="e.g., Apple",
        help="Type a name and press Enter to search."
    )
    
    if not company_name:
        return None

    with st.spinner("Searching..."):
        search_results = search_for_ticker(company_name)

    if not search_results:
        st.error("Search failed or returned no results.", icon="❌")
        return None

    ticker_options = {
        f"{res.get('longname', res.get('shortname', 'N/A'))} ({res['symbol']})": res['symbol']
        for res in search_results if 'symbol' in res and res.get('quoteType') == 'EQUITY'
    }

    if not ticker_options:
        st.info("No valid stock tickers found for your query.", icon="ℹ️")
        return None

    selected_option = st.selectbox(
        "Select the correct company:",
        options=list(ticker_options.keys()),
        key=f"{key_prefix}_select"
    )
    return ticker_options.get(selected_option)

def create_comparison_table(info1, info2, ticker1, ticker2):
    """Creates a side-by-side comparison table with highlighting."""
    data = []
    for display_name, key in FINANCIAL_METRICS.items():
        if key is None:
            data.append({"Metric": f"**{display_name}**", ticker1: '', ticker2: '', 'raw1': None, 'raw2': None})
            continue
        val1, val2 = info1.get(key), info2.get(key)
        data.append({
            "Metric": display_name,
            ticker1: format_metric_value(val1, display_name),
            ticker2: format_metric_value(val2, display_name),
            'raw1': val1,
            'raw2': val2
        })

    df_full = pd.DataFrame(data).set_index('Metric')
    df_display = df_full[[ticker1, ticker2]]

    def highlight_better(row):
        """Applies styling by looking up raw values from the full dataframe."""
        styles = [''] * 2
        
        raw_values = df_full.loc[row.name]
        val1, val2 = raw_values['raw1'], raw_values['raw2']

        if not isinstance(val1, (int, float)) or not isinstance(val2, (int, float)):
            return styles
            
        lower_is_better = ["Trailing P/E", "Forward P/E", "PEG Ratio", "Price/Book (P/B)", "EV/Revenue", "EV/EBITDA", "Debt/Equity", "Payout Ratio"]
        winner_style = 'background-color: #1A3C34; color: #A7D7C5;'
        
        is_lower_better_metric = row.name in lower_is_better
        
        if (is_lower_better_metric and val1 < val2) or (not is_lower_better_metric and val1 > val2):
            styles[0] = winner_style
        elif (is_lower_better_metric and val2 < val1) or (not is_lower_better_metric and val2 > val1):
            styles[1] = winner_style
            
        return styles
    
    styler = df_display.style.apply(highlight_better, axis=1)
    st.dataframe(styler, use_container_width=True)

def display_advanced_metrics(results: dict):
    """Displays the advanced metrics in columns."""
    cols = st.columns(3)
    metric_map = {
        'valuation': ("Valuation (Forward P/E)", "Based on Forward P/E. Lower is generally better. Good < 15, Fair < 25, Overvalued >= 25."),
        'profitability': ("Profitability", "Based on Return on Equity (ROE > 15%)."),
        'health': ("Financial Health (D/E)", "Based on Debt to Equity ratio. A lower ratio (< 100) suggests less risk."),
        'pb': ("Price-to-Book (P/B)", "Compares market price to the company's book value. A ratio < 1 may indicate an undervalued stock."),
        'dividend': ("Dividend Yield", "Shows the dividend as a percentage of the stock price. The delta shows the payout ratio."),
        'growth': ("Revenue Growth (YoY)", "Shows the year-over-year revenue growth. Positive growth is a healthy sign."),
    }
    
    for i, key in enumerate(metric_map):
        with cols[i % 3]:
            res = results.get(key, {})
            st.metric(
                label=metric_map[key][0],
                value=res.get('value', 'N/A'),
                delta=res.get('delta', 'N/A'),
                delta_color=res.get('delta_color', 'off'),
                help=metric_map[key][1]
            )
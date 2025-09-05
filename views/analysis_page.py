"""Handles the layout and logic for the main stock analysis page."""

import streamlit as st
import pandas as pd
from datetime import date, timedelta

# Import from custom modules
from constants import CURRENCY_SYMBOLS
from data_utils import get_stock_data, get_exchange_rate
from analysis import metrics, conclusion
from ui import components

def initialize_session_state():
    """Initializes session state variables if they don't exist."""
    defaults = {
        'start_date': date.today() - timedelta(days=365),
        'end_date': date.today(),
        'current_ticker': None,
        'stock_info': None,
        'historical_data': None,
        'last_fetch_start': None,
        'last_fetch_end': None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def manage_toast_notifications():
    """Displays and clears any queued toast messages for date changes."""
    if st.session_state.get('toast_message'):
        st.toast(st.session_state.toast_message, icon="🗓️")
        st.session_state.toast_message = None

def display_sidebar_content():
    """Renders all sidebar components and returns the selected ticker."""
    with st.sidebar:
        # --- REFINED LAYOUT & WORDING ---
        st.markdown("## 🛠️ App Controls")

        st.markdown("### Find a Stock")
        search_method = st.radio("Search Method", ("Top Companies", "Search by Company/Ticker"), key="search_method", label_visibility="collapsed")

        if search_method == "Top Companies":
            tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NFLX", "NVDA", "V", "JPM", "GS"]
            selected_ticker = st.selectbox("Ticker Symbol", tickers)
        else:
            selected_ticker = components.company_search_box("Company Name", "analysis")

        st.markdown("### 🗓️ Time Period")
        st.date_input("From", key='start_date', max_value=date.today())
        st.date_input("To", key='end_date', max_value=date.today())
        components.render_date_range_buttons()

        info = st.session_state.get('stock_info')
        if info:
            st.markdown("### ⚙️ Display Options")
            stock_currency = info.get("currency", "USD")
            
            prev_currency = st.session_state.get('selected_currency')
            components.render_currency_converter(stock_currency)
            new_currency = st.session_state.get('selected_currency')

            if prev_currency and prev_currency != new_currency:
                st.toast(f"Currency updated to {new_currency}", icon="💱")


        st.markdown("---")        
        st.markdown("<div style='text-align: center; font-size: 0.85em;'>Made with ❤️ by <strong>Sandeep</strong></div>", unsafe_allow_html=True)
                
    return selected_ticker

# --- The functions display_main_content() and display() remain the same as your last version ---
def display_main_content(ticker: str, info: dict, historical_data: pd.DataFrame | None):
    """Renders the main content area with charts, metrics, and details."""
    selected_currency = st.session_state.get('selected_currency', info.get("currency", "USD"))
    exchange_rate = get_exchange_rate(info.get("currency", "USD"), selected_currency)
    currency_symbol = CURRENCY_SYMBOLS.get(selected_currency, "$")

    if exchange_rate is None:
        exchange_rate = 1.0
        currency_symbol = CURRENCY_SYMBOLS.get(info.get("currency", "USD"), "$")

    st.markdown(f"## {info.get('longName', 'N/A')} ({ticker})")
    current_price, previous_close = info.get("currentPrice"), info.get("previousClose")
    if all(isinstance(i, (int, float)) for i in [current_price, previous_close, exchange_rate]):
        st.metric(
            label=f"Current Price ({selected_currency})",
            value=f"{currency_symbol}{current_price * exchange_rate:,.2f}",
            delta=f"{currency_symbol}{(current_price - previous_close) * exchange_rate:,.2f}"
        )
    else:
        st.metric(label=f"Current Price ({selected_currency})", value="Data not available")

    chart_tab, metrics_tab, details_tab, advanced_tab = st.tabs([
        "📈 Historical Price", "📊 Financial Metrics", "🏢 Company Details", "⭐ Advanced Indicators"
    ])
    with chart_tab:
        if historical_data is not None:
            chart_type = st.radio("Select Chart Type:", ("Candlestick", "Line", "Line with Moving Averages", "Area"), horizontal=True)
            components.create_price_chart(historical_data, ticker, exchange_rate, currency_symbol, chart_type)
        else:
            st.info("No historical price data available to display.")
    with metrics_tab: components.display_financial_metrics(info, exchange_rate, currency_symbol)
    with details_tab:
        st.markdown(f"### About {info.get('longName', 'N/A')}")
        st.markdown(f"**Sector:** {info.get('sector', 'N/A')} | **Industry:** {info.get('industry', 'N/A')}")
        st.markdown("---"); st.write(info.get("longBusinessSummary", "No business summary available."))
    with advanced_tab:
        st.markdown("### Special Key Indicators")
        advanced_results, analysis_summary = metrics.analyze_advanced_metrics(info)
        components.display_advanced_metrics(advanced_results)
        st.markdown("---"); st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(conclusion.generate_conclusion(analysis_summary), unsafe_allow_html=True)

def display():
    """The main display function for the Stock Analysis page."""
    initialize_session_state()
    manage_toast_notifications()

    selected_ticker = display_sidebar_content()
    
    main_content_placeholder = st.empty()

    if not selected_ticker:
        main_content_placeholder.info("Please select a ticker or search for a company in the sidebar.")
        st.session_state.current_ticker = None
        return

    if not st.session_state.start_date or not st.session_state.end_date:
        main_content_placeholder.error("Please provide a valid start and end date in the sidebar.")
        return
        
    if st.session_state.start_date > st.session_state.end_date:
        main_content_placeholder.error("Error: The start date cannot be after the end date. Please select a valid range.")
        return

    needs_fetch = (
        st.session_state.current_ticker != selected_ticker or
        st.session_state.last_fetch_start != st.session_state.start_date or
        st.session_state.last_fetch_end != st.session_state.end_date
    )

    if needs_fetch:
        with main_content_placeholder.container():
            st.markdown(f"<div style='text-align: center; font-size: 1.5em;'>📈 Fetching new data for <strong>{selected_ticker}</strong>...</div>", unsafe_allow_html=True)
            with st.spinner("Connecting to financial markets and gathering historical data..."):
                info_data, historical_data = get_stock_data(
                    selected_ticker,
                    st.session_state.start_date,
                    st.session_state.end_date
                )
                st.session_state.current_ticker = selected_ticker
                st.session_state.stock_info = info_data
                st.session_state.historical_data = historical_data
                st.session_state.last_fetch_start = st.session_state.start_date
                st.session_state.last_fetch_end = st.session_state.end_date
        st.rerun()
    else:
        info = st.session_state.stock_info
        historical_data = st.session_state.historical_data
        
        with main_content_placeholder.container():
            if info:
                display_main_content(selected_ticker, info, historical_data)
            else:
                st.error(f"Could not retrieve valid data for '{selected_ticker}'.")
import streamlit as st
import pandas as pd
from datetime import date, timedelta
from config import CURRENCY_SYMBOLS, TOP_TICKERS, APP_CONFIG
from data import get_stock_data, get_exchange_rate
from utils.analysis import metrics, conclusion
from ui import (
    company_search_box,
    render_date_range_buttons,
    render_currency_converter,
    create_price_chart,
    display_financial_metrics,
    display_advanced_metrics,
    show_loading_spinner,
)

def initialize_session_state():
    defaults = {
        'start_date': date.today() - timedelta(days=APP_CONFIG["default_date_range_days"]),
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
    if st.session_state.get('toast_message'):
        st.toast(st.session_state.toast_message, icon="🗓️")
        st.session_state.toast_message = None

def display_sidebar_content():
    with st.sidebar:
        st.markdown("## 🛠️ App Controls")
        st.markdown("### Find a Stock")
        search_method = st.radio(
            "Search Method",
            ("Top Companies", "Search by Company/Ticker"),
            key="search_method",
            label_visibility="collapsed"
        )

        if search_method == "Top Companies":
            selected_ticker = st.selectbox("Ticker Symbol", TOP_TICKERS)
        else:
            selected_ticker = company_search_box("Company Name", "analysis")

        st.markdown("### 🗓️ Time Period")
        st.date_input("From", key='start_date', max_value=date.today())
        st.date_input("To", key='end_date', max_value=date.today())
        render_date_range_buttons()

        info = st.session_state.get('stock_info')
        if info:
            st.markdown("### ⚙️ Display Options")
            stock_currency = info.get("currency", "USD")
            render_currency_converter(stock_currency)

        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; font-size: 0.85em;'>Made with ❤️ by <strong>Sandeep</strong></div>",
            unsafe_allow_html=True
        )

    return selected_ticker

def display_main_content(ticker: str, info: dict, historical_data: pd.DataFrame | None):
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


    chart_tab, metrics_tab, details_tab, advanced_tab = st.tabs(
        ["📈 Historical Price", "📊 Financial Metrics", "🏢 Company Details", "⭐ Advanced Indicators"]
    )

    with chart_tab:
        if historical_data is not None:
            chart_type = st.radio(
                "Select Chart Type:",
                ("Candlestick", "Line", "Line with Moving Averages", "Area"),
                horizontal=True
            )
            create_price_chart(historical_data, ticker, exchange_rate, currency_symbol, chart_type)
        else:
            st.info("No historical price data available to display.")

    with metrics_tab:
        display_financial_metrics(info, exchange_rate, currency_symbol)

    with details_tab:
        st.markdown(f"### About {info.get('longName', 'N/A')}")
        st.markdown(f"**Sector:** {info.get('sector', 'N/A')} | **Industry:** {info.get('industry', 'N/A')}")
        st.markdown("---")
        st.write(info.get("longBusinessSummary", "No business summary available."))

    with advanced_tab:
        st.markdown("### Special Key Indicators")
        advanced_results, analysis_summary = metrics.analyze_advanced_metrics(info)
        display_advanced_metrics(advanced_results)
        st.markdown("---")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(conclusion.generate_conclusion(analysis_summary), unsafe_allow_html=True)

def display():
    initialize_session_state()
    manage_toast_notifications()

    selected_ticker = display_sidebar_content()

    if st.session_state.get('currency_toast'):
        st.toast(st.session_state.currency_toast, icon="💱")
        st.session_state.currency_toast = None

    # Main content placeholder (the only container we will use)
    main_content_placeholder = st.empty()

    # If nothing is selected yet
    if not selected_ticker:
        main_content_placeholder.info("Please select a ticker or search for a company in the sidebar.")
        st.session_state.current_ticker = None
        return

    # Validate dates
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
        # 🔒 Ensure the main area is BLANK during load
        main_content_placeholder.empty()  # remove any prior content

        # Show ONLY the spinner (no content rendered beneath it)
        with show_loading_spinner("Connecting to financial markets and gathering historical data..."):
            info_data, historical_data = get_stock_data(
                selected_ticker,
                st.session_state.start_date,
                st.session_state.end_date
            )
            # Update session state after fetch completes
            st.session_state.current_ticker = selected_ticker
            st.session_state.stock_info = info_data
            st.session_state.historical_data = historical_data
            st.session_state.last_fetch_start = st.session_state.start_date
            st.session_state.last_fetch_end = st.session_state.end_date

        # Force a clean render AFTER data arrives (spinner ends)
        st.rerun()

    else:
        info = st.session_state.stock_info
        historical_data = st.session_state.historical_data

        # Render content only when we have data and we are not loading
        with main_content_placeholder.container():
            if info:
                display_main_content(selected_ticker, info, historical_data)
            else:
                st.error(f"Could not retrieve valid data for '{selected_ticker}'.")

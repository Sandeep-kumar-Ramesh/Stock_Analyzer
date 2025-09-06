import streamlit as st
from datetime import date, timedelta
from config import CURRENCY_SYMBOLS, TOP_TICKERS
from data import search_for_ticker
from .loading import show_loading_spinner

def _set_date_range(days: int, label: str):
    st.session_state.end_date = date.today()
    st.session_state.start_date = date.today() - timedelta(days=days)
    st.session_state.toast_message = f"Date range set to the last {label}."

def _reset_dates():
    _set_date_range(365, "year")

def render_date_range_buttons():
    col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
    with col1: st.button("Reset", on_click=_reset_dates, use_container_width=True)
    with col2: st.button("1M", on_click=_set_date_range, args=(30, "month"), use_container_width=True)
    with col3: st.button("3M", on_click=_set_date_range, args=(90, "3 months"), use_container_width=True)
    with col4: st.button("6M", on_click=_set_date_range, args=(180, "6 months"), use_container_width=True)

def _currency_change_callback():
    if hasattr(st.session_state, 'previous_currency') and st.session_state.previous_currency != st.session_state.selected_currency:
        st.session_state.currency_toast = f"Currency updated to {st.session_state.selected_currency}"
    st.session_state.previous_currency = st.session_state.selected_currency

def render_currency_converter(stock_currency: str):
    currency_options = list(CURRENCY_SYMBOLS.keys())
    try:
        default_index = currency_options.index(stock_currency)
    except ValueError:
        default_index = 0
    
    if 'selected_currency' not in st.session_state:
        st.session_state.selected_currency = stock_currency
        st.session_state.previous_currency = stock_currency
    
    st.selectbox(
        "Display currency:",
        currency_options,
        index=default_index,
        key="selected_currency",
        on_change=_currency_change_callback
    )

def company_search_box(label: str, key_prefix: str) -> str | None:
    company_name = st.text_input(
        "Enter company name or ticker:",
        key=f"{key_prefix}_name",
        placeholder="e.g., Apple",
        help="Type a name and press Enter to search."
    )
    
    if not company_name:
        return None

    with show_loading_spinner("🔍 Searching for companies..."):
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

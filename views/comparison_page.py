"""Handles the layout and logic for the stock comparison page."""

import streamlit as st
from data_utils import get_stock_info
from ui import components

def display_sidebar():
    """Renders the sidebar for the comparison page."""
    with st.sidebar:
        st.header("🛠️ Comparison Control")
        ticker1 = components.company_search_box("Stock 1", "comp1")
        st.markdown("---")
        ticker2 = components.company_search_box("Stock 2", "comp2")
    return ticker1, ticker2

def display():
    """The main display function for the Comparison page."""
    ticker1, ticker2 = display_sidebar()
    st.header("Compare Two Stocks Side-by-Side")
    main_content_placeholder = st.empty()

    if not ticker1 or not ticker2:
        main_content_placeholder.info("Please select two stocks from the sidebar to begin comparison.")
        return

    if ticker1 == ticker2:
        main_content_placeholder.error("Please select two different stocks to compare.")
        return

    # FIX 3: Enhanced Spinner UI for comparison
    with main_content_placeholder.container():
        with st.spinner("Crunching the numbers for your Analysis..."):
            info1 = get_stock_info(ticker1)
            info2 = get_stock_info(ticker2)

        if info1 and info2:
            st.markdown(f"### {info1.get('shortName')} vs. {info2.get('shortName')}")
            components.create_comparison_table(info1, info2, ticker1, ticker2)
        else:
            if not info1: st.error(f"Could not fetch data for {ticker1}.")
            if not info2: st.error(f"Could not fetch data for {ticker2}.")
import streamlit as st
from data import get_stock_info
from ui import company_search_box, create_comparison_table, show_loading_spinner

def display_sidebar():
    with st.sidebar:
        st.header("🛠️ Comparison Control")
        ticker1 = company_search_box("Stock 1", "comp1")
        st.markdown("---")
        ticker2 = company_search_box("Stock 2", "comp2")
        st.markdown("---")
        
        # Compare button with custom styling
        if st.button("🔍 Compare Stocks", use_container_width=True, type="secondary"):
            st.session_state.compare_clicked = True
        else:
            st.session_state.compare_clicked = False
            
    return ticker1, ticker2

def display():
    ticker1, ticker2 = display_sidebar()
    st.header("Compare Two Stocks Side-by-Side")
    main_content_placeholder = st.empty()

    if not ticker1 or not ticker2:
        main_content_placeholder.info("Please select two stocks from the sidebar to begin comparison.")
        return

    if ticker1 == ticker2:
        main_content_placeholder.error("Please select two different stocks to compare.")
        return

    # Only show comparison when compare button is clicked
    if st.session_state.get('compare_clicked', False):
        with main_content_placeholder.container():
            with show_loading_spinner("🔄 Crunching the numbers for your Analysis..."):
                info1 = get_stock_info(ticker1)
                info2 = get_stock_info(ticker2)

            if info1 and info2:
                st.markdown(f"### {info1.get('shortName')} vs. {info2.get('shortName')}")
                create_comparison_table(info1, info2, ticker1, ticker2)
            else:
                if not info1: st.error(f"Could not fetch data for {ticker1}.")
                if not info2: st.error(f"Could not fetch data for {ticker2}.")
    else:
        main_content_placeholder.info("Click the 'Compare Stocks' button in the sidebar to start the comparison.")
# 📄 app.py

"""The main entry point for the Streamlit Stock Analyzer application."""

import streamlit as st
from streamlit_option_menu import option_menu
from datetime import date, timedelta

# Import from custom modules
from constants import CURRENCY_SYMBOLS
from data_utils import get_stock_data, get_stock_info, get_exchange_rate
from analysis import analyze_advanced_metrics, generate_conclusion
from ui_components import (
    display_financial_metrics, create_price_chart,
    company_search_box, create_comparison_table,
    reset_dates, set_date_range
)

# --- Page and Styling Configuration ---
st.set_page_config(
    page_title="Stock Analyzer",
    page_icon=":material/trending_up:",
    layout="wide",
)

# --- CSS Styling ---
# In app.py

# --- CSS Styling ---
st.markdown("""
<style>
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
  [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
      background-color: rgb(50 103 145) !important;
  }
  [data-testid="stSidebar"] {
      color: #ffffff !important;
  }
  div[data-testid="stTabs"] div[role="tablist"] {
      display: flex;
      justify-content: space-evenly;
      width: 100%;
  }
  div[data-testid="stTabs"] button[role="tab"] {
      flex-grow: 1;
  }
  /* --- NEW: Rule to make all tab text bolder --- */
  button[data-baseweb="tab"] p {
      font-weight: 700 !important;
  }
  [data-testid="stSidebar"] div[data-testid="stButton"] button {
      padding: 2px 8px !important;
      font-size: 0.8rem !important;
      height: auto !important;
      min-height: 0 !important;
      margin: 0 !important;
  }
  /* --- UPDATED: Changed selected tab color to the main blue --- */
  button[data-baseweb="tab"][aria-selected="true"] {
      border-bottom-color: rgb(50 103 145) !important;
      color: rgb(50 103 145) !important;
  }
  div[data-testid="stRadio"] [aria-checked="true"] > div:first-child {
      border-color: #0078D4 !important;
  }
  div[data-testid="stRadio"] [aria-checked="true"] > div > div {
      background-color: #0078D4 !important;
  }
  div[data-testid="stMetric"] {
      background-color: #273342;
      border: 1px solid #273342;
      border-radius: 8px;
      padding: 15px;
  }
  div[data-testid="stMetric"] > label {
      display: flex;
      align-items: center;
      justify-content: space-between;
  }
</style>
""", unsafe_allow_html=True)


# --- Main Application Layout ---

def main():
    st.title("Stock Analyzer :material/trending_up:")
    st.markdown("Your **:blue[personal]** financial analysis dashboard. :material/insights:")

    selected = option_menu(
        menu_title=None, 
        options=["Stock Analysis", "Compare Stocks"],
        icons=["search", "columns-gap"], 
        default_index=0, 
        orientation="horizontal",
        styles={
            # We remove the container padding to let the links define the space
            "container": {"padding": "0!important", "background-color": "#0e1117"},
            "nav-link": {
                "font-size": "16px",
                "padding": "10px 20px", # Increased padding for more height
                "text-align": "center",
                "margin": "0px 4px", # Adds a small gap between buttons
                "--hover-color": "#273342" # Adds a subtle hover effect
            },
            "nav-link-selected": {
                "background-color": "rgb(50 103 145)",
                "font-weight": "600",
            },
        }
    )
    
    if selected == "Stock Analysis":
        run_stock_analysis_page()
    elif selected == "Compare Stocks":
        run_comparison_page()

def run_stock_analysis_page():
    """Renders the main stock analysis page."""
    # This initialization is correct and should be kept.
    if 'start_date' not in st.session_state: 
        st.session_state.start_date = date.today() - timedelta(days=365)
    if 'end_date' not in st.session_state: 
        st.session_state.end_date = date.today()

    with st.sidebar:
        st.header("App Settings")
        search_method = st.radio("Select search method:", ("Ticker", "Company Name"), key="search_method")
        if search_method == "Ticker":
            tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NFLX", "NVDA", "V", "JPM", "GS"]
            selected_ticker = st.selectbox("Select a stock ticker:", tickers)
        else:
            selected_ticker = company_search_box("Search by Company Name", "analysis")
        
        st.markdown("---")
        st.subheader("Chart Date Range")
        
        # FIX APPLIED: Removed the 'value' argument to rely on session state via the 'key'.
        start_date_val = st.date_input(
            "Start date:", 
            min_value=date(1980, 1, 1), 
            max_value=date.today(), 
            key='start_date'
        )
        end_date_val = st.date_input(
            "End date:", 
            min_value=start_date_val, 
            max_value=date.today(), 
            key='end_date'
        )
        
        if not start_date_val or not end_date_val:
            st.error("Please provide a valid start and end date.")
            st.stop()
        
        col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
        with col1: st.button("Reset", on_click=reset_dates, use_container_width=True)
        with col2: st.button("1M", on_click=set_date_range, args=(30, "month"), use_container_width=True)
        with col3: st.button("3M", on_click=set_date_range, args=(90, "3 months"), use_container_width=True)
        with col4: st.button("6M", on_click=set_date_range, args=(180, "6 months"), use_container_width=True)

    if not selected_ticker:
        st.info("Please select a ticker or search for a company in the sidebar.")
        return

    main_content_placeholder = st.empty()
    with st.spinner(f"Fetching data for {selected_ticker}..."):
        info, historical_data = get_stock_data(selected_ticker, start_date_val, end_date_val)
    
    if info is None:
        st.error(f"Could not retrieve valid data for '{selected_ticker}'. The ticker may be incorrect, delisted, or there was a network issue.")
        return
    
    if historical_data is None:
        st.toast("Could not retrieve historical data for the selected date range.", icon="📈")

    with main_content_placeholder.container():
        with st.sidebar:
            st.markdown("---"); st.subheader("Currency Converter")
            stock_currency = info.get("currency", "USD")
            currency_options = list(CURRENCY_SYMBOLS.keys())
            default_index = currency_options.index(stock_currency) if stock_currency in currency_options else 0
            
            prev_currency = st.session_state.get('selected_currency', stock_currency)
            selected_currency = st.selectbox("Display currency:", currency_options, index=default_index, key="currency_selector")
            
            if prev_currency != selected_currency:
                st.toast(f"Currency updated to {selected_currency}", icon="💱")
            st.session_state.selected_currency = selected_currency

            exchange_rate = get_exchange_rate(stock_currency, selected_currency)
            currency_symbol = CURRENCY_SYMBOLS.get(selected_currency, "$")

            if exchange_rate is None:
                st.toast(f"Could not fetch exchange rate. Displaying in original currency ({stock_currency}).", icon="⚠️")
                exchange_rate = 1.0
                currency_symbol = CURRENCY_SYMBOLS.get(stock_currency, "$")

        st.markdown(f"## {info.get('longName', 'N/A')} ({selected_ticker})")
        
        current_price, previous_close = info.get("currentPrice"), info.get("previousClose")
        if all(isinstance(i, (int, float)) for i in [current_price, previous_close, exchange_rate]):
            st.metric(
                label=f"Current Price ({selected_currency})", 
                value=f"{currency_symbol}{current_price * exchange_rate:,.2f}", 
                delta=f"{currency_symbol}{(current_price - previous_close) * exchange_rate:,.2f}"
            )
        else:
            st.metric(label=f"Current Price ({selected_currency})", value="Data not available")
        
        chart_tab, metrics_tab, details_tab, advanced_tab = st.tabs(["📈 Historical Price", "📊 Financial Metrics", "🏢 Company Details", "⭐ Advanced Indicators"])
        
        with chart_tab:
            if historical_data is not None:
                chart_type = st.radio("Select Chart Type:", ("Candlestick", "Line", "Line with Moving Averages", "Area"), horizontal=True, key="chart_type_selector")
                create_price_chart(historical_data, selected_ticker, exchange_rate, currency_symbol, chart_type)
            else:
                st.info("No historical price data available to display.")
        
        with metrics_tab: display_financial_metrics(info, exchange_rate, currency_symbol)
        with details_tab:
            st.markdown(f"### About {info.get('longName', 'N/A')}")
            st.markdown(f"**Sector:** {info.get('sector', 'N/A')} | **Industry:** {info.get('industry', 'N/A')}")
            st.markdown("---"); st.write(info.get("longBusinessSummary", "No business summary available."))
        
        with advanced_tab:
            st.markdown("### Special Key Indicators")
            
            advanced_results, scores, pros, cons = analyze_advanced_metrics(info)

            cols = st.columns(3)
            metric_map = {
                0: ('valuation', "Valuation (Forward P/E)", "Based on Forward P/E. Lower is generally better. Good < 15, Fair < 25, Overvalued >= 25."),
                1: ('profitability', "Profitability", "Combines Return on Equity (ROE > 15%) and Gross Margins (> 40%)."),
                2: ('health', "Financial Health (D/E)", "Based on Debt to Equity ratio. A lower ratio (< 100) suggests less risk."),
                3: ('pb', "Price-to-Book (P/B)", "Compares market price to the company's book value. A ratio < 1 may indicate an undervalued stock."),
                4: ('dividend', "Dividend Yield", "Shows the dividend as a percentage of the stock price. The delta shows the payout ratio."),
                5: ('growth', "Revenue Growth (YoY)", "Shows the year-over-year revenue growth. Positive growth is a healthy sign."),
            }
            
            for i, res_key in enumerate(metric_map):
                with cols[i % 3]:
                    res = advanced_results[metric_map[res_key][0]]
                    st.metric(label=metric_map[res_key][1], value=res['value'], delta=res['delta'], delta_color=res['delta_color'], help=metric_map[res_key][2])

            st.markdown("---"); st.markdown("<br>", unsafe_allow_html=True)
            analysis_data = {"scores": scores, "pros": pros, "cons": cons}
            st.markdown(generate_conclusion(analysis_data), unsafe_allow_html=True)

def run_comparison_page():
    """Renders the stock comparison page."""
    with st.sidebar:
        st.header("Comparison Settings")
        ticker1 = company_search_box("Stock 1", "comp1")
        st.markdown("---")
        ticker2 = company_search_box("Stock 2", "comp2")
    
    st.header("Compare Two Stocks Side-by-Side")
    if ticker1 and ticker2:
        if ticker1 == ticker2:
            st.error("Please select two different stocks to compare.")
        else:
            with st.spinner(f"Fetching data for {ticker1} and {ticker2}..."):
                info1 = get_stock_info(ticker1)
                info2 = get_stock_info(ticker2)
            if info1 and info2:
                st.markdown(f"### {info1.get('shortName')} vs. {info2.get('shortName')}")
                create_comparison_table(info1, info2, ticker1, ticker2)
            else:
                if not info1: st.error(f"Could not fetch data for {ticker1}.")
                if not info2: st.error(f"Could not fetch data for {ticker2}.")
    else:
        st.info("Please select two stocks from the sidebar to begin comparison.")

if __name__ == "__main__":
    main()
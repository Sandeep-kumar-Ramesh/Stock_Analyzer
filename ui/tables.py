import streamlit as st
import pandas as pd
from typing import Dict, Any
from config import FINANCIAL_METRICS, CURRENCY_SYMBOLS

def format_metric_value(value: Any, metric_name: str = "", currency_symbol: str = "$", rate: float = 1.0) -> str:
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

def display_financial_metrics(info: Dict[str, Any], exchange_rate: float, currency_symbol: str):
    data = []
    for display_name, key in FINANCIAL_METRICS.items():
        if key is None:
            data.append({"Metric": display_name, "Value": ''})
            continue
        value = info.get(key)
        formatted_value = format_metric_value(value, display_name, currency_symbol, exchange_rate)
        data.append({"Metric": display_name, "Value": formatted_value})

    df = pd.DataFrame(data)
    styler = df.style.apply(
        lambda row: ['font-weight: bold; color: #0078D4; text-align: left; font-size: 1.1em;', ''] if str(row['Metric']) in ['VALUATION', 'PROFITABILITY & MARGINS', 'GROWTH & FINANCIAL HEALTH', 'DIVIDENDS'] else ['', ''],
        axis=1
    ).set_table_styles([
        {'selector': 'thead th', 'props': [('color', '#0078D4'), ('font-weight', 'bold'), ('font-size', '1.1em')]}
    ])
    with st.expander("Key Financial Metrics", expanded=True):
        st.dataframe(styler, use_container_width=True, hide_index=True)

def create_comparison_table(info1, info2, ticker1, ticker2):
    data = []
    for display_name, key in FINANCIAL_METRICS.items():
        if key is None:
            data.append({"Metric": display_name, ticker1: '', ticker2: '', 'raw1': None, 'raw2': None})
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
    
    styler = df_display.style.apply(highlight_better, axis=1).set_table_styles([
        {'selector': 'thead th', 'props': [('color', '#0078D4'), ('font-weight', 'bold'), ('font-size', '1.1em')]}
    ])
    st.dataframe(styler, use_container_width=True)

def display_advanced_metrics(results: dict):
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

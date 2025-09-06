import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def create_price_chart(historical_data: pd.DataFrame, ticker: str, exchange_rate: float, currency_symbol: str, chart_type: str):
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

"""Module for UI styling and CSS."""
import streamlit as st

def apply_custom_css():
    """Applies custom CSS to the Streamlit app."""
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
          border: 1px solid #30363D;
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
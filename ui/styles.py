import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      
      /* Fixed sidebar width and non-draggable */
      [data-testid="stSidebar"] {
          width: 300px !important;
          min-width: 300px !important;
          max-width: 300px !important;
          color: #ffffff !important;
          resize: none !important;
      }
      
      [data-testid="stSidebar"][aria-expanded="true"] {
          width: 300px !important;
          min-width: 300px !important;
          max-width: 300px !important;
      }
      
      [data-testid="stSidebar"][aria-expanded="false"] {
          width: 0px !important;
          min-width: 0px !important;
          max-width: 0px !important;
      }
      
      [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
          background-color: rgb(50 103 145) !important;
          width: 300px !important;
      }
      
      /* Adjust main content area based on sidebar state */
      .main .block-container {
          padding-left: 1rem !important;
          padding-right: 1rem !important;
      }
      
      /* When sidebar is expanded */
      [data-testid="stSidebar"][aria-expanded="true"] ~ .main .block-container {
          margin-left: 300px !important;
          max-width: calc(100vw - 300px) !important;
      }
      
      /* When sidebar is collapsed */
      [data-testid="stSidebar"][aria-expanded="false"] ~ .main .block-container {
          margin-left: 0px !important;
          max-width: 100vw !important;
      }
      
      /* Remove resize handle and disable dragging */
      [data-testid="stSidebar"] .resize-handle {
          display: none !important;
      }
      
      /* Disable cursor changes and dragging */
      [data-testid="stSidebar"] {
          cursor: default !important;
          user-select: none !important;
          -webkit-user-select: none !important;
          -moz-user-select: none !important;
          -ms-user-select: none !important;
      }
      
      [data-testid="stSidebar"] * {
          cursor: default !important;
      }
      
      /* Prevent drag events */
      [data-testid="stSidebar"] {
          pointer-events: auto !important;
      }
      
      /* Remove any drag-related styling */
      [data-testid="stSidebar"]:hover {
          background-color: inherit !important;
      }
      
      [data-testid="stSidebar"][aria-expanded="true"]:hover {
          background-color: rgb(50 103 145) !important;
      }
      
      /* Tab styling */
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
      
      /* Button styling in sidebar */
      [data-testid="stSidebar"] div[data-testid="stButton"] button {
          padding: 2px 8px !important;
          font-size: 0.8rem !important;
          height: auto !important;
          min-height: 0 !important;
          margin: 0 !important;
      }
      
      /* Compare button styling in sidebar */
      [data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"] {
          background-color: #ffffff !important;
          color: rgb(50 103 145) !important;
          border: 2px solid #ffffff !important;
          font-weight: 600 !important;
          border-radius: 8px !important;
          transition: all 0.3s ease !important;
      }
      
      [data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"]:hover {
          background-color: #f0f0f0 !important;
          color: rgb(50 103 145) !important;
          border-color: #f0f0f0 !important;
          transform: translateY(-1px) !important;
      }
      
      /* Tab selection styling */
      button[data-baseweb="tab"][aria-selected="true"] {
          border-bottom-color: rgb(50 103 145) !important;
          color: rgb(50 103 145) !important;
      }
      
      /* Radio button styling */
      div[data-testid="stRadio"] [aria-checked="true"] > div:first-child {
          border-color: #0078D4 !important;
      }
      div[data-testid="stRadio"] [aria-checked="true"] > div > div {
          background-color: #0078D4 !important;
      }
      
      /* Metric styling */
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
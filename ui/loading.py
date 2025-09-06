import streamlit as st
from contextlib import contextmanager

@contextmanager
def show_loading_spinner(message="Loading..."):
    """Shows a circular loading spinner with custom message."""
    with st.spinner(message):
        yield

@contextmanager
def with_loading_spinner(message="Loading..."):
    """Context manager to add loading spinner to any code block."""
    with st.spinner(message):
        yield

def show_loading_progress(message="Fetching data..."):
    """Shows a progress bar with custom message."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        progress_bar.progress(i + 1)
        status_text.text(f"{message} {i+1}%")
        time.sleep(0.01)  # Small delay for visual effect
    
    progress_bar.empty()
    status_text.empty()

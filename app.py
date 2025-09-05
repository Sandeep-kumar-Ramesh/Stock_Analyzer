"""The main entry point for the Streamlit Stock Analyzer application."""

import streamlit as st
from streamlit_option_menu import option_menu

# Import page handlers and UI styles
from views import analysis_page, comparison_page  # CHANGED HERE
from ui.styles import apply_custom_css

def main():
    """Main function to configure and run the Streamlit app."""
    # --- Page and Styling Configuration ---
    st.set_page_config(
        page_title="Stock Analyzer",
        page_icon=":material/trending_up:",
        layout="wide",
    )
    apply_custom_css()

    st.title("Stock Analyzer :material/trending_up:")
    st.markdown(":material/insights: Your **:blue[personal]** financial analysis dashboard for powerful financial insights. Unlock smarter investment decisions.")

    # --- Main Navigation ---
    pages = {
        "Stock Analysis": {
            "icon": "search",
            "func": analysis_page.display
        },
        "Compare Stocks": {
            "icon": "columns-gap",
            "func": comparison_page.display
        },
    }

    selected = option_menu(
        menu_title=None,
        options=list(pages.keys()),
        icons=[pages[x]["icon"] for x in pages],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#0e1117"},
            "nav-link": {
                "font-size": "16px",
                "padding": "10px 20px",
                "text-align": "center",
                "margin": "0px 4px",
                "--hover-color": "#273342"
            },
            "nav-link-selected": {
                "background-color": "rgb(50, 103, 145)",
                "font-weight": "600",
            },
        }
    )

    # Run the selected page's display function
    if selected and selected in pages:
        pages[selected]["func"]()

if __name__ == "__main__":
    main()
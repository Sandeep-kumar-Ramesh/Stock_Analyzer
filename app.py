import streamlit as st
from streamlit_option_menu import option_menu
from config import APP_CONFIG, NAVIGATION_CONFIG
from views import analysis_display, comparison_display
from ui import apply_custom_css

def main():
    st.set_page_config(
        page_title=APP_CONFIG["page_title"],
        page_icon=APP_CONFIG["page_icon"],
        layout=APP_CONFIG["layout"],
    )
    apply_custom_css()

    st.title("Stock Analyzer :material/trending_up:")
    st.markdown(":material/insights: Your **:blue[personal]** financial analysis dashboard for powerful financial insights. Unlock smarter investment decisions.")

    pages = {
        "Stock Analysis": {
            "icon": "search",
            "func": analysis_display
        },
        "Compare Stocks": {
            "icon": "columns-gap",
            "func": comparison_display
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

    if selected and selected in pages:
        pages[selected]["func"]()

if __name__ == "__main__":
    main()
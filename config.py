FINANCIAL_METRICS = {
    "Market Cap": "marketCap",
    "Enterprise Value": "enterpriseValue",
    "VALUATION": None,
    "Trailing P/E": "trailingPE",
    "Forward P/E": "forwardPE",
    "PEG Ratio": "pegRatio",
    "Price/Book (P/B)": "priceToBook",
    "EV/Revenue": "enterpriseToRevenue",
    "EV/EBITDA": "enterpriseToEbitda",
    "PROFITABILITY & MARGINS": None,
    "Return on Equity (ROE)": "returnOnEquity",
    "Profit Margins": "profitMargins",
    "Operating Margins": "operatingMargins",
    "Gross Margins": "grossMargins",
    "GROWTH & FINANCIAL HEALTH": None,
    "Revenue Growth (YoY)": "revenueGrowth",
    "Debt/Equity": "debtToEquity",
    "Total Cash": "totalCash",
    "Total Debt": "totalDebt",
    "DIVIDENDS": None,
    "Dividend Yield": "dividendYield",
    "Payout Ratio": "payoutRatio",
}

CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "INR": "₹",
    "CHF": "Fr"
}

TOP_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NFLX", "NVDA", "V", "JPM", "GS"]

APP_CONFIG = {
    "page_title": "Stock Analyzer",
    "page_icon": ":material/trending_up:",
    "layout": "wide",
    "default_date_range_days": 365
}

NAVIGATION_CONFIG = {
    "Stock Analysis": {
        "icon": "search",
        "module": "views.analysis_page"
    },
    "Compare Stocks": {
        "icon": "columns-gap", 
        "module": "views.comparison_page"
    }
}

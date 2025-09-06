# 📈 Stock Analyzer

A powerful, modern web application for comprehensive stock analysis and comparison built with Streamlit.

## ✨ Features

### 🔍 **Stock Analysis**
- **Real-time Data**: Live stock prices and historical data
- **Interactive Charts**: Candlestick, Line, Moving Averages, and Area charts
- **Financial Metrics**: Comprehensive financial ratios and KPIs
- **Advanced Indicators**: Technical analysis with scoring system
- **Multi-currency Support**: View prices in USD, EUR, GBP, JPY, and more

### 📊 **Stock Comparison**
- **Side-by-side Analysis**: Compare two stocks simultaneously
- **Key Metrics Comparison**: Financial ratios, performance indicators
- **Visual Comparison**: Easy-to-read comparison tables

### 🎨 **Modern UI/UX**
- **Responsive Design**: Fixed sidebar with expandable/collapsible functionality
- **Loading States**: Beautiful circular spinners during data fetching
- **Toast Notifications**: Real-time feedback for user actions
- **Professional Styling**: Clean, modern interface with blue accent colors

### 🚀 **Smart Features**
- **Company Search**: Search by company name or ticker symbol
- **Date Range Selection**: Flexible time period analysis
- **Currency Conversion**: Real-time exchange rate conversion
- **Cached Data**: Fast performance with intelligent caching

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Data Source**: Yahoo Finance API (yfinance)
- **Charts**: Plotly
- **Data Processing**: Pandas
- **Styling**: Custom CSS

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Stock_Analyzer-stock_analyzer
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Start analyzing stocks! 🎉

## 📱 How to Use

### Stock Analysis
1. **Select a Stock**: Choose from top companies or search by name
2. **Set Date Range**: Pick your analysis period
3. **Choose Currency**: Select your preferred display currency
4. **Explore**: View charts, metrics, and advanced indicators

### Stock Comparison
1. **Navigate**: Go to "Compare Stocks" page
2. **Select Stocks**: Choose two different stocks
3. **Compare**: Click "Compare Stocks" button
4. **Analyze**: Review side-by-side comparison


## 🔧 Configuration

Edit `config.py` to customize:
- Default date ranges
- Top ticker symbols
- Currency options
- App settings

## 📈 Sample Usage

1. **Analyze Apple (AAPL)**:
   - Select "Top Companies" → "AAPL"
   - Set date range to "1M"
   - View candlestick chart and financial metrics

2. **Compare Tech Giants**:
   - Go to "Compare Stocks"
   - Search for "Apple" and "Microsoft"
   - Click "Compare Stocks" to see side-by-side analysis

---

**Made with ❤️ by Sandeep**

*Happy Trading! 📈🚀*

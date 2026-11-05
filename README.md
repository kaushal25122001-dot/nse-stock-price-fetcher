# NSE Indian Stocks 30-Day Closing Prices Pipeline & Web Dashboard

A complete, production-ready full-stack Python and web analytics application designed to extract, analyze, visualize, and export the past 30 days of daily closing prices for four top Indian blue-chip stocks on the **National Stock Exchange (NSE)**.

---

## 📈 Target Stocks

| Company Name | NSE Ticker Symbol | Sector |
| :--- | :--- | :--- |
| **HDFC Bank** | `HDFCBANK.NS` | Banking & Financial Services |
| **Reliance Industries** | `RELIANCE.NS` | Conglomerate / Energy & Telecom |
| **TCS** | `TCS.NS` | Information Technology |
| **ITC** | `ITC.NS` | Fast-Moving Consumer Goods (FMCG) |

---

## 🖥️ Frontend Web Dashboard Features

The project includes an interactive frontend dashboard (`index.html`) featuring:

1. **Live Stock Metric Cards**:
   - Real-time badges for all four companies showing latest closing price (₹), 30-day net return (₹ and %), and 30-day high/low boundaries.
2. **Interactive Performance Chart**:
   - **Normalized Return Mode (% Return)**: Re-indexes all 4 assets to a 0% baseline to compare true relative capital growth over the 30-day window.
   - **Actual Price Mode (₹)**: Displays raw split- and dividend-adjusted INR values.
   - Crosshair hover tooltips with exact session date and closing figures.
3. **Searchable Matrix Table**:
   - Clean tabular view of daily closing prices.
   - Real-time date filter (`YYYY-MM-DD`).
4. **Client-side & Server-side CSV Export**:
   - One-click export button downloading `past_30_days_closing_prices.csv`.

---

## 📁 Project Structure

```text
nse-stock-fetcher/
├── fetch_closing_prices.py          # Core Python data extraction & CSV export script
├── app.py                           # Web server powering the frontend & JSON API
├── index.html                       # Modern interactive financial dashboard UI
├── requirements.txt                 # Python dependencies (yfinance, pandas)
├── README.md                        # Documentation and architecture guide
└── past_30_days_closing_prices.csv  # Generated output CSV dataset
```

---

## 🚀 Quickstart Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. View in Frontend Dashboard
To launch the interactive web dashboard with live auto-refresh and browser integration:
```bash
python app.py
```
> The dashboard will automatically open in your default browser at `http://localhost:8000/index.html`.

*(Alternatively, you can also double-click `index.html` directly in your file explorer to view the interface offline).*

### 3. Run Command-Line Script Only
If you only need to run the data collection and CSV export without the web UI:
```bash
python fetch_closing_prices.py
```

"""
NSE Stock Web Dashboard Server
===============================
Author: Financial Data Analyst & Python Developer
Description:
    Runs a lightweight web server that serves the interactive frontend dashboard
    and provides real-time JSON API endpoints.
    Uses standard library `http.server` to guarantee zero extra web framework setup.
"""

import csv
import http.server
import json
import logging
import os
import socketserver
import urllib.parse
import webbrowser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = "past_30_days_closing_prices.csv"

# Graceful check for yfinance / pandas
try:
    from fetch_closing_prices import (
        TICKER_MAP,
        LOOKBACK_DAYS,
        get_date_range,
        fetch_and_process_stock_data
    )
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False
    logger.info("yfinance or pandas not found in current environment. Running with local CSV cache.")


def read_cached_csv() -> list:
    """Reads the CSV file using standard library csv module."""
    csv_path = os.path.join(DIRECTORY, OUTPUT_CSV)
    if not os.path.exists(csv_path):
        return []

    records = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = {}
            for k, v in row.items():
                if k == "Date":
                    cleaned[k] = v
                else:
                    try:
                        cleaned[k] = float(v)
                    except ValueError:
                        cleaned[k] = v
            records.append(cleaned)
    return records


class StockDashboardHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler serving static dashboard files
    and dynamic financial data API endpoints.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)

        # Redirect root '/' to '/index.html'
        if parsed_url.path in ("/", ""):
            self.send_response(302)
            self.send_header("Location", "/index.html")
            self.end_headers()
            return

        # API endpoint: Return the 30-day closing prices in JSON format
        if parsed_url.path == "/api/stocks":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            records = []
            if HAS_YFINANCE:
                try:
                    start_date, end_date = get_date_range(LOOKBACK_DAYS)
                    df = fetch_and_process_stock_data(TICKER_MAP, start_date, end_date)
                    df.to_csv(os.path.join(DIRECTORY, OUTPUT_CSV))
                    records = df.reset_index().to_dict(orient="records")
                    logger.info(f"Fetched live from Yahoo Finance: {len(records)} trading sessions.")
                except Exception as exc:
                    logger.warning(f"Live fetch failed ({exc}), falling back to cached CSV.")
                    records = read_cached_csv()
            else:
                records = read_cached_csv()

            self.wfile.write(json.dumps(records).encode("utf-8"))
            return

        # Default: Serve static files (index.html, csv, etc.)
        return super().do_GET()


def main():
    print("\n" + "=" * 65)
    print("      NSE Stock Dashboard Server")
    print("=" * 65)

    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True

    dashboard_url = f"http://localhost:{PORT}/index.html"

    with socketserver.TCPServer(("", PORT), StockDashboardHandler) as httpd:
        print(f"\n[SUCCESS] Server is live and accessible at:")
        print(f"  👉  {dashboard_url}")
        print("\nPress Ctrl+C in terminal to stop server.\n")

        # Open web browser automatically
        try:
            webbrowser.open(dashboard_url)
        except Exception:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server. Goodbye!")


if __name__ == "__main__":
    main()

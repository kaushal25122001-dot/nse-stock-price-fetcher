"""
NSE Stock Closing Price Fetcher
================================
Author: Financial Data Analyst & Python Developer
Description:
    Downloads daily closing prices for selected Indian stocks listed on the
    National Stock Exchange (NSE) over the past 30 days using Yahoo Finance (`yfinance`).
    Ensures corporate action adjustments (splits & dividends), remaps tickers
    to friendly company names, displays results in terminal, and exports to CSV.
"""

from datetime import datetime, timedelta
import logging
from typing import Dict
import pandas as pd
import yfinance as yf

# Configure clean logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Configuration & Constants
# ---------------------------------------------------------
# Mapping NSE Yahoo Finance tickers to human-readable company names
TICKER_MAP: Dict[str, str] = {
    "HDFCBANK.NS": "HDFC Bank",
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "TCS",
    "ITC.NS": "ITC"
}

OUTPUT_CSV: str = "past_30_days_closing_prices.csv"
LOOKBACK_DAYS: int = 30


def get_date_range(days: int = LOOKBACK_DAYS) -> tuple[str, str]:
    """
    Dynamically computes the date window (start and end dates) for the query.

    Args:
        days (int): Number of calendar days to look back from today.

    Returns:
        tuple[str, str]: (start_date, end_date) formatted as 'YYYY-MM-DD'.
        Note: In yfinance, 'end' is exclusive. We add 1 day to today's date
        so that today's trading session (if closed) is included.
    """
    today = datetime.now().date()
    start_date = today - timedelta(days=days)
    end_date = today + timedelta(days=1)

    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def fetch_and_process_stock_data(
    ticker_map: Dict[str, str],
    start_date: str,
    end_date: str
) -> pd.DataFrame:
    """
    Downloads historical stock data from Yahoo Finance, extracts clean closing prices,
    and remaps ticker symbols to human-readable company names.

    Args:
        ticker_map (Dict[str, str]): Dictionary mapping ticker symbols to company names.
        start_date (str): Start date string (YYYY-MM-DD).
        end_date (str): End date string (YYYY-MM-DD).

    Returns:
        pd.DataFrame: Cleaned DataFrame of closing prices with readable column headers.
    """
    tickers = list(ticker_map.keys())
    logger.info(f"Initiating download for tickers: {', '.join(tickers)}")
    logger.info(f"Target window: {start_date} to {end_date} (inclusive of current date)")

    try:
        # auto_adjust=True automatically accounts for stock splits and dividend distributions.
        # When auto_adjust=True, the 'Close' column reflects true corporate-action-adjusted prices.
        raw_data = yf.download(
            tickers=tickers,
            start=start_date,
            end=end_date,
            auto_adjust=True,
            progress=False
        )
    except Exception as exc:
        logger.error(f"Failed to fetch data from Yahoo Finance: {exc}")
        raise

    if raw_data.empty:
        raise ValueError("No data returned by yfinance for the specified date range and tickers.")

    # In multi-ticker downloads, raw_data has MultiIndex columns: (PriceAttribute, Ticker)
    # Extract only the 'Close' attribute
    if "Close" in raw_data:
        closing_prices = raw_data["Close"].copy()
    else:
        # Fallback if single ticker or different hierarchy
        closing_prices = raw_data.copy()

    # Remap columns from NSE tickers to readable company names
    closing_prices.rename(columns=ticker_map, inplace=True)

    # Format the DateTime index to clean 'YYYY-MM-DD' strings and rename index
    closing_prices.index = closing_prices.index.strftime("%Y-%m-%d")
    closing_prices.index.name = "Date"

    # Round price figures to 2 decimal places for financial reporting precision
    closing_prices = closing_prices.round(2)

    return closing_prices


def main() -> None:
    """
    Orchestrates the dynamic date calculation, data fetching, console presentation,
    and CSV file export.
    """
    print("\n" + "=" * 65)
    print("      NSE Top Stocks: 30-Day Adjusted Closing Prices")
    print("=" * 65)

    # 1. Compute dynamic date boundaries
    start_str, end_str = get_date_range(LOOKBACK_DAYS)
    logger.info(f"Timeframe: Last {LOOKBACK_DAYS} days [{start_str} to {datetime.now().strftime('%Y-%m-%d')}]")

    # 2. Fetch and sanitize stock closing price data
    try:
        closing_df = fetch_and_process_stock_data(
            ticker_map=TICKER_MAP,
            start_date=start_str,
            end_date=end_str
        )
    except Exception as err:
        logger.error(f"Execution terminated with error: {err}")
        return

    # 3. Neatly print DataFrame to the console
    print("\n--- Daily Closing Prices (INR) ---")
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)
    print(closing_df.to_string())
    print("-" * 65)

    # 4. Export results to CSV
    try:
        closing_df.to_csv(OUTPUT_CSV)
        logger.info(f"Dataset successfully exported to '{OUTPUT_CSV}'")
    except IOError as io_err:
        logger.error(f"Failed to write CSV file '{OUTPUT_CSV}': {io_err}")

    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()


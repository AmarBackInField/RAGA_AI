import yfinance as yf
import pandas as pd
from config.logging_config import setup_logging

# Set up logging
logger = setup_logging(__name__)

def load_stock_data(ticker: str, period: str,interval: str):
    """
    Load historical stock data from Yahoo Finance.

    Parameters:
    - ticker (str): Stock ticker symbol (e.g., 'AAPL' for Apple)
    - period (str):
    - interval (str): Data interval ('1m','2m','5m','15m','1h','1d','1wk','1mo')

    Returns:
    - pandas.DataFrame: Stock data
    """
    try:
        logger.info(f"Fetching stock data for {ticker} .")
        
        # Validate ticker
        if not ticker or not isinstance(ticker, str):
            logger.error("Invalid ticker symbol")
            return None
            
        # Clean ticker symbol
        ticker = ticker.strip().upper()
        
        # # Validate ticker exists
        # stock = yf.Ticker(ticker)
        # info = stock.info
        # if not info or 'regularMarketPrice' not in info:
        #     logger.error(f"Invalid ticker symbol: {ticker}")
        #     return None
            
        # Download data
        data = yf.download("AAPL", period="1mo", interval="1d", auto_adjust=True)
        print(data)

        
        if data.empty:
            logger.warning(f"No data found for {ticker} in the specified date range")
            return None
            
        # Ensure we have the required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in data.columns for col in required_columns):
            logger.error(f"Missing required columns in data for {ticker}")
            return None
            
        # Round numeric columns to 2 decimal places
        numeric_columns = ['Open', 'High', 'Low', 'Close']
        data[numeric_columns] = data[numeric_columns].round(2)
        
        # Format volume as integer
        data['Volume'] = data['Volume'].astype(int)
        
        logger.info(f"Successfully downloaded {len(data)} days of data for {ticker}")
        return data
        
    except Exception as e:
        logger.error(f"Error loading stock data for {ticker}: {str(e)}", exc_info=True)
        return None

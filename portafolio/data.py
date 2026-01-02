import yfinance as yf

TICKERS = [
    "IVV", "VEA", "VWO",
    "MSFT", "NVDA", "GOOGL", "AMZN", "MELI",
    "XOM", "CVX", "UNH", "JNJ", "BIP"
]

def get_prices():
    data = yf.download(TICKERS, period="1d", group_by="ticker", auto_adjust=True)
    prices = {}
    for t in TICKERS:
        prices[t] = float(data[t]["Close"].iloc[-1])
    return prices

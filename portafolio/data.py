import yfinance as yf

TICKERS = ["MSFT", "NVDA", "XOM", "BIP", "MELI"]
CURRENCY = "MXN"

def get_prices():
    data = yf.download(TICKERS, period="1d", group_by="ticker", auto_adjust=True)
    prices = {}
    for t in TICKERS:
        prices[t] = float(data[t]["Close"].iloc[-1])
    return prices

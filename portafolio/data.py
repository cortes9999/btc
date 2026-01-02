import yfinance as yf

TICKERS = ["MSFT", "NVDA", "XOM", "BIP", "MELI", "V"]

def get_prices():
    data = yf.download(TICKERS, period="1d", group_by="ticker")
    return {t: float(data[t]["Close"].iloc[-1]) for t in TICKERS}

def get_positions(prices):
    # Placeholder: 10 acciones de cada una
    return {t: prices[t] * 10 for t in prices}

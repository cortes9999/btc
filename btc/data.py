import requests
import pandas as pd

HISTORICAL_DAYS = 365

def get_btc_history():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": HISTORICAL_DAYS,
        "interval": "daily"
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()

    prices = pd.DataFrame(r.json()["prices"], columns=["ts", "price"])
    prices["date"] = pd.to_datetime(prices["ts"], unit="ms")
    prices.set_index("date", inplace=True)
    return prices["price"]

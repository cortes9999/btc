import requests
import pandas as pd
import time

HISTORICAL_DAYS_PRIMARY = 365
HISTORICAL_DAYS_FALLBACK = 180
MAX_RETRIES = 3
TIMEOUT = 10

HEADERS = {
    "User-Agent": "investment-bot/1.0"
}

def _fetch_history(days):
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }

    r = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()

    prices = pd.DataFrame(r.json()["prices"], columns=["ts", "price"])
    prices["date"] = pd.to_datetime(prices["ts"], unit="ms")
    prices.set_index("date", inplace=True)

    return prices["price"]

def get_btc_history():
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return _fetch_history(HISTORICAL_DAYS_PRIMARY)
        except Exception as e:
            last_error = e
            time.sleep(attempt * 2)

    # fallback más corto
    try:
        return _fetch_history(HISTORICAL_DAYS_FALLBACK)
    except Exception:
        raise RuntimeError(
            "CoinGecko no disponible tras reintentos y fallback"
        ) from last_error

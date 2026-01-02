import requests
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os

# =============================
# CONFIG
# =============================
ANNUAL_BUDGET = 12_000
WEEKLY_BUDGET = ANNUAL_BUDGET / 52
HISTORICAL_DAYS = 365

# =============================
# DATA
# =============================
def get_btc_history():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": HISTORICAL_DAYS, "interval": "daily"}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    prices = pd.DataFrame(r.json()["prices"], columns=["ts", "price"])
    prices["date"] = pd.to_datetime(prices["ts"], unit="ms")
    prices.set_index("date", inplace=True)
    return prices["price"]

# =============================
# INDICATORS
# =============================
def indicators(price):
    df = pd.DataFrame(price, columns=["price"])
    df["ma180"] = df["price"].rolling(180).mean()
    df["ret_8w"] = df["price"].pct_change(56)
    df["vol_6w"] = df["price"].pct_change().rolling(42).std()
    df["max_20w"] = df["price"].rolling(140).max()
    df["dd"] = df["price"] / df["max_20w"] - 1
    return df.dropna()

# =============================
# STRATEGY
# =============================
def market_score(row, vol_thr):
    score = 0
    if row["price"] > row["ma180"]: score += 1
    if row["ret_8w"] > 0: score += 1
    if row["vol_6w"] < vol_thr: score += 1
    if row["dd"] > -0.30: score += 1
    return score

def multiplier(score):
    return {0:0,1:0,2:0.5,3:1.0,4:1.5}[score]

# =============================
# EMAIL
# =============================
def send_email(body):
    msg = MIMEText(body)
    msg["Subject"] = "BTC – Señal Sistemática Semanal"
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = os.environ["EMAIL_TO"]

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
        s.send_message(msg)

# =============================
# MAIN
# =============================
def main():
    price = get_btc_history()
    df = indicators(price)

    last = df.iloc[-1]
    vol_thr = df["vol_6w"].quantile(0.70)
    score = market_score(last, vol_thr)

    usd = WEEKLY_BUDGET * multiplier(score)
    btc = usd / last["price"] if usd > 0 else 0

    body = f"""
BTC – Señal Sistemática Semanal

Fecha: {datetime.utcnow().date()}
Precio BTC (USD): {last['price']:.2f}

Market Score: {score} / 4

Monto a comprar (USD): {usd:.2f}
BTC a comprar: {btc:.6f}

Regla:
- Score ≤ 1 → No comprar
- Score 2 → Compra parcial
- Score ≥ 3 → Compra completa
"""

    send_email(body)

if __name__ == "__main__":
    main()

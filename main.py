import requests
import pandas as pd
import numpy as np
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

    # Estadísticos
    df["z_price"] = (df["price"] - df["ma180"]) / df["price"].rolling(180).std()
    df["ret_daily"] = df["price"].pct_change()
    df["autocorr"] = df["ret_daily"].rolling(30).apply(
        lambda x: x.autocorr(lag=1), raw=False
    )

    return df.dropna()

# =============================
# CORE STRATEGY
# =============================
def market_score(row, vol_thr):
    score = 0
    if row["price"] > row["ma180"]: score += 1
    if row["ret_8w"] > 0: score += 1
    if row["vol_6w"] < vol_thr: score += 1
    if row["dd"] > -0.30: score += 1
    return score

def base_multiplier(score):
    return {0:0, 1:0, 2:0.5, 3:1.0, 4:1.5}[score]

# =============================
# STATISTICAL FILTERS
# =============================
def statistical_adjustment(row):
    """
    Returns adjustment factor and explanation
    """
    factor = 1.0
    notes = []

    if abs(row["z_price"]) > 2:
        factor = 0.0
        notes.append("Z-score extremo (>2): compra bloqueada")

    elif row["autocorr"] < 0:
        factor = 0.5
        notes.append("Autocorrelación negativa: compra reducida 50%")

    if not notes:
        notes.append("Filtros estadísticos favorables")

    return factor, "; ".join(notes)

# =============================
# EMAIL
# =============================
def send_email(body):
    if not all(key in os.environ for key in ["EMAIL_USER", "EMAIL_TO", "EMAIL_PASS"]):
        print("Environment variables EMAIL_USER, EMAIL_TO, EMAIL_PASS not set. Skipping email.")
        return

    msg = MIMEText(body)
    msg["Subject"] = "BTC – Señal Sistemática Semanal (Base vs Robusta)"
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

    # ----- Recomendación BASE -----
    base_usd = WEEKLY_BUDGET * base_multiplier(score)
    base_btc = base_usd / last["price"] if base_usd > 0 else 0

    # ----- Recomendación ROBUSTA -----
    stat_factor, stat_notes = statistical_adjustment(last)
    robust_usd = base_usd * stat_factor
    robust_btc = robust_usd / last["price"] if robust_usd > 0 else 0

    body = f"""
BTC – Señal Sistemática Semanal
Fecha: {datetime.now(datetime.UTC).date()}
Precio BTC (USD): {last['price']:.2f}

================================
1) RECOMENDACIÓN BASE
================================
Market Score: {score} / 4
Monto a comprar (USD): {base_usd:.2f}
BTC a comprar: {base_btc:.6f}

================================
2) RECOMENDACIÓN ROBUSTA
(Core + Filtros Estadísticos)
================================
Ajuste estadístico: {stat_notes}

Monto a comprar (USD): {robust_usd:.2f}
BTC a comprar: {robust_btc:.6f}

Interpretación:
- La sección 1 sigue reglas puramente de régimen
- La sección 2 confirma o bloquea compras en extremos estadísticos
"""

    send_email(body)

if __name__ == "__main__":
    main()

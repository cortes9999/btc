from datetime import datetime, UTC
from btc.data import get_btc_history
from btc.indicators import indicators
from btc.strategy import market_score, base_multiplier, statistical_adjustment
from btc.mail import send_email

ANNUAL_BUDGET = 12_000
WEEKLY_BUDGET = ANNUAL_BUDGET / 52

def main():
    price = get_btc_history()
    df = indicators(price)

    last = df.iloc[-1]
    vol_thr = df["vol_6w"].quantile(0.70)

    score = market_score(last, vol_thr)

    base_usd = WEEKLY_BUDGET * base_multiplier(score)
    base_btc = base_usd / last["price"] if base_usd > 0 else 0.0

    stat_factor, stat_notes = statistical_adjustment(last)
    robust_usd = base_usd * stat_factor
    robust_btc = robust_usd / last["price"] if robust_usd > 0 else 0.0

    body_html = f"""
    <h2>BTC – Señal Sistemática Semanal</h2>
    <p><strong>Fecha:</strong> {datetime.now(UTC).date()}</p>
    <p><strong>Precio BTC:</strong> {last['price']:.2f} USD</p>

    <h3>Base</h3>
    <ul>
      <li>Score: {score}/4</li>
      <li>Monto USD: {base_usd:.2f}</li>
      <li>BTC: {base_btc:.6f}</li>
    </ul>

    <h3>Robusta</h3>
    <p>{stat_notes}</p>
    <ul>
      <li>Monto USD: {robust_usd:.2f}</li>
      <li>BTC: {robust_btc:.6f}</li>
    </ul>
    """

    send_email("BTC – Señal Sistemática Semanal", body_html)

if __name__ == "__main__":
    main()

from datetime import date
import pandas as pd

def record_purchases(ledger_df, allocations, prices):
    rows = []

    for ticker, amount in allocations.items():
        price = prices[ticker]
        units = amount / price

        rows.append({
            "date": date.today().isoformat(),
            "ticker": ticker,
            "action": "BUY",
            "amount_mxn": round(amount, 2),
            "price": round(price, 2),
            "units": round(units, 6)
        })

    return pd.concat([ledger_df, pd.DataFrame(rows)], ignore_index=True)

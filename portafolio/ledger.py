import pandas as pd
from pathlib import Path

LEDGER_PATH = Path("portafolio/ledger.csv")

COLUMNS = ["date", "ticker", "action", "amount_mxn", "price", "units"]

def load_ledger():
    if not LEDGER_PATH.exists():
        return pd.DataFrame(columns=COLUMNS)
    return pd.read_csv(LEDGER_PATH)

def save_ledger(df):
    df.to_csv(LEDGER_PATH, index=False)

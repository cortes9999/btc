import pandas as pd
from pathlib import Path

LEDGER_PATH = Path("portafolio/ledger.csv")

COLUMNS = ["date", "ticker", "action", "amount_mxn", "price", "units"]

def load_ledger():
    if not LEDGER_PATH.exists():
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(LEDGER_PATH, index=False)  # Crea el CSV vacío
        return df
    return pd.read_csv(LEDGER_PATH)


def save_ledger(df):
    df.to_csv(LEDGER_PATH, index=False)

import pandas as pd
from pathlib import Path
import os

# Ruta absoluta desde el root del repo
LEDGER_PATH = Path(os.environ.get("GITHUB_WORKSPACE", ".")) / "portfolio" / "ledger.csv"

COLUMNS = ["date", "ticker", "action", "amount_mxn", "price", "units"]

def load_ledger():
    # Crear carpeta si no existe
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not LEDGER_PATH.exists():
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(LEDGER_PATH, index=False)
        return df

    return pd.read_csv(LEDGER_PATH)


def save_ledger(df):
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(LEDGER_PATH, index=False)

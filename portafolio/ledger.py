import pandas as pd
from pathlib import Path

LEDGER_PATH = Path("portfolio/ledger.csv")
COLUMNS = ["date", "ticker", "action", "amount_mxn", "price", "units"]

def load_ledger():
    """
    Carga el ledger desde CSV.
    Si no existe, lo crea vacío y devuelve el DataFrame.
    """
    if not LEDGER_PATH.exists():
        # Crear carpeta si no existe
        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Crear CSV vacío
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(LEDGER_PATH, index=False)
        return df

    # Si existe, leer CSV
    return pd.read_csv(LEDGER_PATH)


def save_ledger(df):
    """
    Guarda el DataFrame de ledger en CSV.
    """
    # Crear carpeta si no existe
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(LEDGER_PATH, index=False)

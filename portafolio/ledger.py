import pandas as pd
from pathlib import Path

# Carpeta opcional para organizar, se crea si no existe
LEDGER_DIR = Path("portafolio")
LEDGER_DIR.mkdir(parents=True, exist_ok=True)

# Archivo ledger dentro de esa carpeta
LEDGER_PATH = LEDGER_DIR / "ledger.csv"

COLUMNS = ["date", "ticker", "action", "amount_mxn", "price", "units"]

def load_ledger():
    """
    Carga el ledger desde CSV.
    Si no existe, lo crea vacío en la carpeta actual o portafolio/
    """
    if not LEDGER_PATH.exists():
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(LEDGER_PATH, index=False)
        print(f"[INFO] Ledger creado en: {LEDGER_PATH.resolve()}")
        return df

    df = pd.read_csv(LEDGER_PATH)
    print(f"[INFO] Ledger cargado desde: {LEDGER_PATH.resolve()}")
    return df

def save_ledger(df):
    """
    Guarda el DataFrame de ledger en CSV.
    """
    df.to_csv(LEDGER_PATH, index=False)
    print(f"[INFO] Ledger guardado en: {LEDGER_PATH.resolve()}")

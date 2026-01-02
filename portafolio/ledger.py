import pandas as pd
from pathlib import Path

# ROOT_DIR → root del repo
ROOT_DIR = Path(__file__).resolve().parent.parent

# Usar tu carpeta correcta
LEDGER_PATH = ROOT_DIR / "portafolio" / "ledger.csv"

COLUMNS = ["date", "ticker", "action", "amount_mxn", "price", "units"]

def load_ledger():
    """
    Carga o crea el ledger en la carpeta portafolio.
    """
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not LEDGER_PATH.exists():
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(LEDGER_PATH, index=False)
        print(f"[INFO] Ledger creado: {LEDGER_PATH.resolve()}")
        return df

    df = pd.read_csv(LEDGER_PATH)
    print(f"[INFO] Ledger cargado desde: {LEDGER_PATH.resolve()}")
    return df

def save_ledger(df):
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(LEDGER_PATH, index=False)
    print(f"[INFO] Ledger guardado en: {LEDGER_PATH.resolve()}")

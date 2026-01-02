import pandas as pd
from pathlib import Path

# Definir ruta absoluta desde el root del repo
ROOT_DIR = Path(__file__).resolve().parent.parent  # portfolio/ → repo root
LEDGER_PATH = ROOT_DIR / "portfolio" / "ledger.csv"

COLUMNS = ["date", "ticker", "action", "amount_mxn", "price", "units"]

def load_ledger():
    """
    Carga el ledger desde CSV.
    Si no existe, lo crea vacío y devuelve el DataFrame.
    """
    # Crear carpeta si no existe
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
    """
    Guarda el DataFrame de ledger en CSV.
    """
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(LEDGER_PATH, index=False)
    print(f"[INFO] Ledger guardado en: {LEDGER_PATH.resolve()}")

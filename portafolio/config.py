# Presupuesto mensual
MONTHLY_BUDGET = 6000

# Core (ETFs) y Satellite (acciones)
CORE_TARGET = {
    "IVV": 0.40,  # S&P500
    "VEA": 0.15,  # Mercados desarrollados ex-US
    "VWO": 0.10   # Emergentes
}

SATELLITE_TARGET = {
    "MSFT": 0.07,
    "NVDA": 0.07,
    "GOOGL": 0.07,
    "AMZN": 0.07,
    "MELI": 0.07,
    "XOM": 0.07,
    "CVX": 0.07,
    "UNH": 0.07,
    "JNJ": 0.07,
    "BIP": 0.07
}

# Consolidado para el algoritmo
TARGET_WEIGHTS = {**CORE_TARGET, **SATELLITE_TARGET}

# Límites por activo
MAX_WEIGHT_PER_ASSET = 0.07  # 7%
MIN_GAP = 0.01  # No comprar si estamos cerca del target

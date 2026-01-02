def market_score(row, vol_thr):
    score = 0
    if row["price"] > row["ma180"]:
        score += 1
    if row["ret_8w"] > 0:
        score += 1
    if row["vol_6w"] < vol_thr:
        score += 1
    if row["dd"] > -0.30:
        score += 1
    return score

def base_multiplier(score):
    return {0: 0.0, 1: 0.0, 2: 0.5, 3: 1.0, 4: 1.5}[score]

def statistical_adjustment(row):
    factor = 1.0
    notes = []

    if abs(row["z_price"]) > 2:
        factor = 0.0
        notes.append("Z-score extremo (>2): compra bloqueada")
    elif row["autocorr"] < 0:
        factor = 0.5
        notes.append("Autocorrelación negativa: compra reducida 50%")

    if not notes:
        notes.append("Filtros estadísticos favorables")

    return factor, "; ".join(notes)

def compute_values(units, prices):
    values = {t: units[t] * prices[t] for t in units}
    total = sum(values.values())

    weights = (
        {t: v / total for t, v in values.items()}
        if total > 0 else {}
    )

    return values, weights

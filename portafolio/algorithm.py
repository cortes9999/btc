MONTHLY_BUDGET = 6000

TARGET_WEIGHTS = {
    "MSFT": 0.20,
    "NVDA": 0.20,
    "XOM": 0.20,
    "BIP": 0.20,
    "MELI": 0.20
}

MIN_GAP = 0.02  # no comprar si está casi en target

def monthly_allocation(weights):
    gaps = {
        t: TARGET_WEIGHTS[t] - weights.get(t, 0)
        for t in TARGET_WEIGHTS
        if TARGET_WEIGHTS[t] - weights.get(t, 0) > MIN_GAP
    }

    if not gaps:
        return {}

    total_gap = sum(gaps.values())
    allocations = {
        t: MONTHLY_BUDGET * (gap / total_gap)
        for t, gap in gaps.items()
    }

    return allocations

TARGET = 1 / 6
BUY_LIMIT = 0.18
MONTHLY_BUDGET = 6000

def monthly_allocation(values):
    total = sum(values.values())
    weights = {k: v / total for k, v in values.items()}

    gaps = {k: TARGET - w for k, w in weights.items() if w < BUY_LIMIT}

    if not gaps:
        return {}, weights

    ordered = sorted(gaps.items(), key=lambda x: x[1], reverse=True)

    alloc = {}
    if len(ordered) == 1:
        alloc[ordered[0][0]] = MONTHLY_BUDGET
    elif len(ordered) == 2:
        alloc[ordered[0][0]] = MONTHLY_BUDGET * 0.6
        alloc[ordered[1][0]] = MONTHLY_BUDGET * 0.4
    else:
        total_gap = sum(g for _, g in ordered)
        for t, g in ordered:
            alloc[t] = MONTHLY_BUDGET * g / total_gap

    return alloc, weights

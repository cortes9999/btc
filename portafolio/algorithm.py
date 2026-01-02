from portafolio.config import MONTHLY_BUDGET, TARGET_WEIGHTS, MIN_GAP

def monthly_allocation(current_weights):
    """
    Calcula la asignación mensual según gaps entre pesos actuales y target
    Solo asigna presupuesto a activos subponderados.
    """
    gaps = {
        t: TARGET_WEIGHTS[t] - current_weights.get(t, 0)
        for t in TARGET_WEIGHTS
        if TARGET_WEIGHTS[t] - current_weights.get(t, 0) > MIN_GAP
    }

    if not gaps:
        return {}

    # Distribuye el presupuesto proporcional al gap
    total_gap = sum(gaps.values())
    allocations = {
        t: MONTHLY_BUDGET * (gap / total_gap)
        for t, gap in gaps.items()
    }

    return allocations

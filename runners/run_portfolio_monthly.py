from portafolio.data import get_prices
from portafolio.ledger import load_ledger, save_ledger
from portafolio.positions import compute_positions
from portafolio.valuation import compute_values
from portafolio.algorithm import monthly_allocation
from portafolio.record import record_purchases
from portafolio.report import build_report
from portafolio.mail import send_email

def main():
    prices = get_prices()

    ledger = load_ledger()
    units = compute_positions(ledger)

    values, weights = compute_values(units, prices)

    allocations = monthly_allocation(weights)

    if allocations:
        ledger = record_purchases(ledger, allocations, prices)
        save_ledger(ledger)

    body = build_report(values, weights, allocations)
    send_email("Portafolio – Ejecución Mensual", body)

if __name__ == "__main__":
    main()

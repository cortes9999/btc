from portfolio.data import get_prices, get_positions
from portfolio.algorithm import monthly_allocation
from portfolio.report import build_report
from portfolio.mail import send_email

def main():
    prices = get_prices()
    values = get_positions(prices)

    allocations, weights = monthly_allocation(values)
    body = build_report(weights, allocations)

    send_email("Portafolio – Ejecución Mensual", body)

if __name__ == "__main__":
    main()

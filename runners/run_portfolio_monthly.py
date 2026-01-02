from portafolio.data import get_prices, get_positions
from portafolio.algorithm import monthly_allocation
from portafolio.report import build_report
from portafolio.mail import send_email

def main():
    prices = get_prices()
    values = get_positions(prices)

    allocations, weights = monthly_allocation(values)
    body = build_report(weights, allocations)

    send_email("Portafolio – Ejecución Mensual", body)

if __name__ == "__main__":
    main()

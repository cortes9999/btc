def build_report(values, weights, allocations):
    html = "<h2>Portafolio – Ejecución Mensual</h2>"

    html += "<h3>Pesos actuales</h3><ul>"
    for t, w in weights.items():
        html += f"<li>{t}: {w:.2%}</li>"
    html += "</ul>"

    html += "<h3>Asignación del mes</h3><ul>"
    for t, a in allocations.items():
        html += f"<li>{t}: ${a:,.2f} MXN</li>"
    html += "</ul>"

    total = sum(allocations.values())
    html += f"<p><strong>Total invertido:</strong> ${total:,.2f} MXN</p>"

    return html

from decimal import Decimal

COMMISSION_TIERS = [
    (Decimal("10000"), Decimal("0.10")),
    (Decimal("5000"),  Decimal("0.07")),
    (Decimal("1000"),  Decimal("0.05")),
    (Decimal("0"),     Decimal("0.00")),
]

def calculate_commission(total):
    """Devuelve (porcentaje, comisión)."""
    for min_amount, rate in COMMISSION_TIERS:
        if total >= min_amount:
            return rate, (total * rate).quantize(Decimal("0.01"))
    return Decimal("0"), Decimal("0.00")
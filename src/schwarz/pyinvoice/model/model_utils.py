
from decimal import ROUND_HALF_UP, Decimal


def round_half_up(value: Decimal) -> Decimal:
    return value.quantize(Decimal('0.01'), ROUND_HALF_UP)

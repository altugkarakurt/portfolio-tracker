from decimal import Decimal
from portfolioapp.config import get_settings


settings = get_settings()
Numeral = int | float | Decimal

# Generates a Decimal from any suitable type to be used as monetary value
# and fixes the resolution to 10^(-settings.decimal_precision), (default=4)
def decimal_from_numeral(num: Numeral) -> Decimal:
    num_dec = Decimal(num)
    template = Decimal(10) ** -(settings.decimal_precision)
    return num_dec.quantize(template)


def weighted_average(items:list[tuple[float, Decimal]]) -> Decimal:
    pass

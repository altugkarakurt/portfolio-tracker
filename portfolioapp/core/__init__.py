from decimal import getcontext, Decimal


DECIMAL_PRECISION = 4

def decimal_from_numeral(num: float|int|Decimal ) -> Decimal:
    num_dec = Decimal(num)
    template = Decimal(10) ** -DECIMAL_PRECISION
    return num_dec.quantize(template)


from portfolioapp.core import Money
from portfolioapp.config import get_settings
from decimal import Decimal

settings = get_settings()

def test_money_init_default():
    # Initializing with all default arguments
    m = Money()
    assert(m.value == 0)
    assert(m.currency == settings.default_currency)

def test_money_init():
    # Tests the model_validator
    money_list = [Money(value=100), Money(value=Decimal(100)), Money(value=100.0)]
    assert(all([m.value == 100 for m in money_list]))

def test_money_comparison():
    # Tests the equality check
    m1 = Money(value=100, currency="USD")
    m2 = Money(value=100, currency="CAD")
    m3 = Money(value=-100, currency="USD")
    assert(m1 != m2)
    assert(m1 != m3)
    assert(m1 >= m3)
    assert(m1 > m3)

def test_money_arithmetic():
    # Tests arithmetic operations
    m1 = Money(value=100)
    m2 = Money(value=-100)
    m3 = Money(value=200)

    assert(-m1 == m2)    # __neg__
    assert(m1*2 == m3)   # __mul__
    assert(-2*m2 == m3)  # __rmul__
    assert(m1+m1 == m3)  # __add__
    assert(m1-m2 == m3)  # __sub__
    assert(m3 / 2 == m1) # __truediv__



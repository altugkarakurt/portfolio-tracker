from portfolioapp.core import Money, Currency
from portfolioapp import config

def test_money_default():
    m = Money()
    assert(m.value == 0)
    assert(m.currency == config["DEFAULT_CURRENCY"])

def test_money():
    # Positive value, default currency
    m1,m2,m3 = Money(value=100), Money(value="100"), Money(value=100.0)
    assert(m1.value == 100)
    assert(m1 == m2 and m2 == m3)

    # Negative value, default currency


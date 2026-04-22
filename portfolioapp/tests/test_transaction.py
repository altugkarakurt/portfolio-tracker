from portfolioapp.core import (
    Equity,
    Money,
    Transaction,
    TransactionType,
)
from portfolioapp.config import get_settings


settings = get_settings()

def test_transaction_init():
    # Initializing with all default arguments
    t1 = Transaction(equity=Equity(symbol="AAPL"),
                     cost=100,
                     units=10,
                     transaction_type="BUY")
    t2 = Transaction(equity=Equity(symbol="AAPL"),
                     cost=Money(value=100),
                     units=10,
                     transaction_type=TransactionType.BUY)
    assert(t1.equity == t2.equity)
    assert(t1.cost == t2.cost)
    assert(t1.transaction_type == t2.transaction_type)

"""
def test_money_init():
    # Tests the model_validator
    money_list = [Money(value=100), Money(value="100"), Money(value=100.0)]
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

def test_money_convert():
    # Tests currency conversion
    m_usd = Money(value=100, currency="USD")
    m_cad = m_usd.convert("CAD")
    
    assert(m_usd == m_cad.convert("USD"))
"""

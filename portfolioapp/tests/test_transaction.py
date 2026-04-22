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


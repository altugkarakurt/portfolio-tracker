# pyright: reportArgumentType=false

from portfolioapp.core import (
    Equity,
    Money,
    Transaction,
    TransactionType,
)
from portfolioapp.config import get_settings


settings = get_settings()

def test_transaction_init():
    # without initializing internal classes
    t1 = Transaction(equity={"symbol":"AAPL"},
                     cost=100,
                     units=10.0,
                     transaction_type="BUY"
    )

    # first initializing the internal classes
    t2 = Transaction(equity=Equity(symbol="AAPL"),
                     cost=Money(value=100),
                     units=10,
                     transaction_type=TransactionType.BUY
    )

    assert(t1.equity == t2.equity)
    assert(t1.cost == t2.cost)
    assert(t1.transaction_type == t2.transaction_type)

def test_signed_units():
    t = Transaction(equity={"symbol":"AAPL"},
                    cost=105,
                    units=10.5,
                    transaction_type="BUY"
    )
    assert(t.signed_units == 10.5)

    t = Transaction(equity={"symbol":"AAPL"},
                    cost=100,
                    units=10.5,
                    transaction_type="SHORT_COVER"
    )
    assert(t.signed_units == 10.5)

    t = Transaction(equity={"symbol":"AAPL"},
                    cost=100,
                    units=10.5,
                    transaction_type="SELL"
    )
    assert(t.signed_units == -10.5)

    t = Transaction(equity={"symbol":"AAPL"},
                    cost=100,
                    units=10.5,
                    transaction_type="SHORT_SELL"
    )
    assert(t.signed_units == -10.5)

def test_per_cost():
    t = Transaction(equity={"symbol":"AAPL"},
                    cost=105,
                    units=10.5,
                    transaction_type="BUY"
    )
    assert(t.per_cost == Money(value=10.0))

def test_is_position_increasing():
    t = Transaction(equity={"symbol":"AAPL"},
                    cost=105,
                    units=10.5,
                    transaction_type="BUY"
    )
    assert(t.is_position_increasing)

    t = Transaction(equity={"symbol":"AAPL"},
                    cost=100,
                    units=10.5,
                    transaction_type="SHORT_SELL"
    )
    assert(t.is_position_increasing)

    t = Transaction(equity={"symbol":"AAPL"},
                    cost=100,
                    units=10.5,
                    transaction_type="SELL"
    )
    assert(not t.is_position_increasing)

    t = Transaction(equity={"symbol":"AAPL"},
                    cost=100,
                    units=10.5,
                    transaction_type="SHORT_COVER"
    )
    assert(not t.is_position_increasing)


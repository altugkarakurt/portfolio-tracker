from .core import Equity, Transaction
from .portfolio import Position, Portfolio
import pandas as pd
from typing import Any, cast


def from_transaction_csv(csvfile:str): # -> Portfolio:
    """
    equity: Equity
    cost: Money
    units: float
    transaction_date: date = Field(
        default_factory=lambda: datetime.now(timezone.utc).date()
    )
    transaction_type: TransactionType
    """
    df = pd.read_csv(csvfile)
    
    # defaultdict is intentionally omitted to prevent creating empty positions
    # for look-ups by the user. We only want to create records with the first
    # transaction for the given equity.
    transactions_by_equity: dict[Equity,list[Transaction]] = dict()
    
    for _,row in df.iterrows():
        # Restructuring the parsed entry
        transaction_dict = row
        transaction_dict["equity"] = {"symbol":transaction_dict["equity"]}
        transaction_dict["cost"] = {"value": transaction_dict["cost"]}
        
        # Explicit type-casting to inform static validation
        transaction = Transaction(**cast(dict[str, Any], transaction_dict))
        if((equity := transaction.equity) in transactions_by_equity.keys()):
            transactions_by_equity[equity].append(transaction)
        else:
            transactions_by_equity[equity] = [transaction]

    positions = [Position(equity=e, transactions=p) for e,p in transactions_by_equity.items()]
    
    return Portfolio(positions=positions)

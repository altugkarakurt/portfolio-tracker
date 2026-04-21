from pydantic import BaseModel, Field
from portfolioapp.core import Money, Equity, Transaction


class Position(BaseModel):
    """------------------------------------------------------------------------
    A mutable data class to store a position in an equity (stock/ETF)
    ---------------------------------------------------------------------------
    equity : Equity
    units : float
        Negative if SELL/SHORT_SELL, positive if BUY/SHORT_COVER
    avg_cost : Money
    transaction_date : date
        The resolution is in days
    transaction_type : TransactionType
    ------------------------------------------------------------------------"""

    equity: Equity
    transactions: list[Transaction] = Field(default_factory=list)
    units: float = 0
    avg_cost: Money = Money()

    @property
    def is_open(self) -> bool:
        return self.units != 0

    @property
    def cost_basis(self) -> Money:
        return self.avg_cost*self.units

    @property
    def market_value(self) -> Money:
        return self.equity.quote() * self.units

    @property
    def realized_gain(self):
        # for t in self.transactions:
        pass

    def add_transaction(self, transaction: Transaction) -> None:
        if(self.equity != transaction.equity):
            raise ValueError(f"Transaction equity {transaction.equity} doesn't \
                             match position equity {self.equity}")
        self.avg_cost = (self.avg_cost * self.units + transaction.cost) \
                        / (self.units + transaction.units)
        self.units += transaction.units
        self.transactions.append(transaction)


class Portfolio(BaseModel):
    positions:list[Position]

    def summary(self):
        print(f"There are {len(self.positions)} and \
              {sum([1 for p in self.positions if(p.is_open)])} are open.")
        for p in self.positions:
            print(f"{p.equity} - Size:{p.units}, Avg Cost:{p.avg_cost}, Current Price:{p.equity.quote()}\n, \
                  \tCost basis:{p.avg_cost*p.units}, Market Value:{p.market_value}")

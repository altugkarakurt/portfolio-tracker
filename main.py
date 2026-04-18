from portfolioapp.core.asset import Money, Currency, Equity, StockExchange
from decimal import Decimal

def main():
    """
    print("Initializing")
    m1 = Money(value="30000.0", currency=Currency.USD)
    m2 = Money(value=50000.0, currency=Currency.CAD)
    m3 = Money(value=Decimal("10123.456"), currency=Currency.USD)
    print(f"from str:{m1=}, from double={m2=}, from dec={m3=}")
    print("-------------------")
    print("Arithmetic")
    print(f"{(m1+m3)=}")
    print(f"{(m1+m2)=}")
    print(f"{(m2+m1)=}")
    print(f"{(m2-m1)=}")
    print("-------------------")
    print(f"left twice: {(2*m2)=}")
    print(f"right negative thrice: {(m2*-3)=}")
    print(f"negative: {(-m1)=}")

    print(f"Clean print: {str(m2)} {str(m1)}")
    """

    t = Equity(symbol="CPNG", exchange=StockExchange.NYSE)
    print(t.fast_query())


if __name__ == "__main__":
    main()

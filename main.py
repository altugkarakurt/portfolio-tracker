from portfolioapp.core.asset import Money, Currency

def main():
    print("Initializing")
    m1 = Money(value=3.0, currency=Currency.USD)
    m2 = Money(value=5.0, currency=Currency.CAD)
    print(f"{m1=}, {m2=}")
    print("-------------------")
    print(f"sum money: {(m1+m2)=}")
    print(f"sum money: {(m2+m1)=}")
    print(f"sub money: {(m2-m1)=}")
    print("-------------------")
    print(f"left twice: {(2*m2)=}")
    print(f"right negative thrice: {(m2*-3)=}")


if __name__ == "__main__":
    main()

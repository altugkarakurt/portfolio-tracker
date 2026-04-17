from portfolioapp.core.asset import Money, Currency

def main():
    print("Hello from portfolio-app!")
    m1 = Money(value=3.0, currency=Currency.USD)
    m2 = Money(value=5.0, currency=Currency.CAD)
    print(f"{m1=}, {m2=}")
    print(f"sum money: {(m1+m2)=}")
    print(f"sum money: {(m2+m1)=}")


if __name__ == "__main__":
    main()

from portfolioapp.parse import from_transaction_csv


def main():
    df = from_transaction_csv("test.csv")
    print(str(df))


if __name__ == "__main__":
    main()

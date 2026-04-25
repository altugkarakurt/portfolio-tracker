# pyright: reportArgumentType=false

from portfolioapp.core import Equity, StockExchange
from portfolioapp.config import get_settings


settings = get_settings()

def test_equity_default():
    # Tests initializing with all default arguments
    e = Equity(symbol="AAPL")
    assert(e.symbol == "AAPL")
    assert(e.exchange == settings.default_exchange)

def test_equity_ticker():
    # Tests the model_validator that generates tickers
    e = Equity(symbol="ABX", exchange="TSX")
    assert(e.ticker.endswith(StockExchange.TSX.suffix))

def test_equity_quote():
    e = Equity(symbol="AAPL")
    price = e.quote()
    assert(price == e.quote()) # Price should never change due to caching

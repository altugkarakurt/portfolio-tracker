from cachetools import cached, TTLCache
from datetime import (
    date,
    datetime,
    timezone,
)
from decimal import Decimal
from enum import StrEnum
from forex_python.converter import CurrencyRates
from typing import (
    Annotated,
    Any,
    cast,
    Self,
)
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)
import yfinance as yf
from portfolioapp.config import get_settings
from portfolioapp.utils import (
    Numeral,
    decimal_from_numeral,
)


settings = get_settings()

def money_from_numeral(num: Money|Numeral) -> Money:
    if(isinstance(num, Money)):
        return num
    return Money(value=decimal_from_numeral(num))


class Currency(StrEnum):
    USD = "USD"
    CAD = "CAD"
    EUR = "EUR"
    GBP = "GBP"


class Money(BaseModel):
    """------------------------------------------------------------------------
    An immutable data class that stores money in a given currency. Implements
    currency conversion and arithmethic.
    ---------------------------------------------------------------------------
    value : int
        The stored value. Originally passed as a float, but internally stored
        as an int representing "numbers of ten thousandths of cents" (10^-4).
        If the constructor is called with an int value, we assume that this
        conversion is already done; real value = (int value)/10^4
    currency : Currency
        The currency the value is in.
    ------------------------------------------------------------------------"""
    model_config = ConfigDict(frozen=True) # makes all instance var.s immutable
    value: Annotated[Decimal, BeforeValidator(decimal_from_numeral)] = Decimal(0)
    currency: Currency = Currency(settings.default_currency)

    @field_validator("value", mode="before")
    @classmethod
    def validate_value(cls, value:Numeral) -> Decimal:
        return decimal_from_numeral(value)

    def __str__(self) -> str:
        match self.currency:
            case Currency.USD:
                symbol = "$"
            case Currency.CAD:
                symbol = "C$"
            case Currency.EUR:
                symbol = "€"
            case Currency.GBP:
                symbol = "£"
        return f"{symbol}{self.value:,.2f}"
    
    def __repr__(self) -> str:
        return f"Money({self.value:,.2f}, {str(self.currency)})"

    # TODO: The dunder methods are returning Money instead of Self due to static
    #       type-checker errors, but that's the right way
    def __add__(self,other:Money) -> Money:
        if(self.currency != other.currency):
            return self + other.convert(target=self.currency)
        return Money(value=(self.value + other.value), currency=self.currency)

    def __sub__(self,other:Money) -> Money:
        return self + (-other)

    def __mul__(self, other:Numeral) -> Money:
        other_val = other if(isinstance(other, Decimal)) else decimal_from_numeral(other)
        return Money(value=(self.value*other_val), currency=self.currency)

    def __rmul__(self, other:Numeral) -> Money:
        return self * other

    def __truediv__(self, other:Numeral) -> Money:
        return Money(value=self.value / decimal_from_numeral(other), currency=self.currency)

    def __neg__(self):
        return self*-1

    def convert(self, target:Currency) -> Money:
        if(self.currency == target):
            return Money(value=self.value, currency=target)
        rate = self.exchange_rate(self.currency, target)
        return Money(value=(self.value*rate),currency=target)

    def __lt__(self, other:Money) -> bool:
        return (self.currency == other.currency and self.value < other.value)

    def __le__(self, other:Money) -> bool:
        return (self < other or self == other)

    @classmethod
    @cached(cache=TTLCache(maxsize=100, ttl=3600))
    def exchange_rate(cls, 
                      from_currency: Currency, 
                      to_currency: Currency) -> Decimal:
        """
            Interface for retrieving currency exchange rates. The rates are
            cached for an hour to minimize server class. Should return Decimal
        """
        return cast(Decimal,CurrencyRates(force_decimal=True).get_rate(from_currency, to_currency))


class StockExchange(StrEnum):
    NYSE   = "NYSE"
    NASDAQ = "NASDAQ"
    TSX    = "TSX"
    TSXV   = "TSXV"
    LSE    = "LSE"
    OTC    = "OTC"

    @property
    def suffix(self):
        match (self):
            case (StockExchange.NYSE | StockExchange.NASDAQ | StockExchange.OTC):
                return ""
            case StockExchange.TSX:
                return ".TO"
            case StockExchange.TSXV:
                return ".V"
            case StockExchange.LSE:
                return ".L"


class Commodity(StrEnum):
    WTI         = "CL=F"
    BRENT       = "BZ-F"
    NATURAL_GAS = "NG=F"
    GOLD        = "GC=F"
    SILVER      = "SI=F"
    COPPER      = "HG=F"
    PLATINUM    = "PL=F"
    PALLADIUM   = "PA=F"


class Equity(BaseModel):
    """------------------------------------------------------------------------
    An immutable data class that stores an equity (stock/ETF for now)
    ---------------------------------------------------------------------------
    symbol : str
    exchange : StockExchange
        The currency the value is in.
    is_etf: bool
        True if this is an ETF/Index Fund, False if this is a company stock.
    ---------------------------------------------------------------------------
    ticker : post-processed version of the symbol, translated to yfinance
             format. ETFs get a prefix "^", while non-US stocks get a suffix
    ------------------------------------------------------------------------"""
    symbol: str
    exchange: StockExchange = StockExchange(settings.default_exchange)
    is_etf: bool = False
    ticker: str = ""
    model_config = ConfigDict(frozen=True)

    @model_validator(mode="after")
    def generate_ticker(self) -> Self:
        prefix = "^" if(self.is_etf) else ""
        ticker = f"{prefix}{self.symbol}{self.exchange.suffix}"

        # Use object.__setattr__ to bypass the frozen restriction
        object.__setattr__(self, 'ticker', ticker)
        return self

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self) -> str:
        return f"Equity({self.ticker})"

    @cached(cache=TTLCache(maxsize=100, ttl=300))
    def fast_query(self) -> dict[str, Any]:
        """
            Query for the latest data for this equity. The responses are
            cached for 5 minutes to reduce traffic
        """
        fields = ["currency", "exchange", "last_price", "market_cap",
                  "day_high", "day_low"]
        data = yf.Ticker(self.ticker).fast_info
        return { field:data[field] for field in fields }

    @cached(cache=TTLCache(maxsize=100, ttl=300))
    def full_query(self) -> dict[str, Any]:
        """
            Query for the latest data for this equity. The responses are
            cached for 5 minutes to reduce traffic
        """
        data = yf.Ticker(self.ticker)
        return data.info

    def quote(self) -> Money:
        response = self.fast_query()
        return Money(value=response["last_price"], currency=response["currency"])


class TransactionType(StrEnum):
    BUY = "BUY"
    SELL = "SELL"
    SHORT_SELL = "SHORT_SELL"
    SHORT_COVER = "SHORT_COVER"


class Transaction(BaseModel):
    """------------------------------------------------------------------------
    An immutable data class to store a transaction (stock/ETF buy/sell/short)
    ---------------------------------------------------------------------------
    equity : Equity
    cost : Money
        Total amount. Positive if SELL/SHORT_SELL, negative if BUY/SHORT_COVER
    units: float
        Negative if SELL/SHORT_SELL, positive if BUY/SHORT_COVER
    transaction_date : date
        The resolution is in days
    transaction_type : TransactionType
    ------------------------------------------------------------------------"""
    model_config = ConfigDict(frozen=True) # makes all instance var.s immutable
    equity: Equity
    cost: Annotated[Money, BeforeValidator(money_from_numeral)]
    units: float
    transaction_date: date = Field(
        default_factory=lambda: datetime.now(timezone.utc).date()
    )
    transaction_type: TransactionType

    @field_validator("transaction_date", mode="before")
    @classmethod
    def validate_date(cls, t_date:(str|date)) -> date:
        if(isinstance(t_date, str)):
            return datetime.strptime(t_date, settings.default_time_format).date()
        return t_date

    @property
    def signed_units(self) -> float:
        return self.units if(self.transaction_type in (TransactionType.BUY, TransactionType.SHORT_COVER)) \
                          else -1*self.units

    @property
    def is_position_increasing(self) -> bool:
        return (self.transaction_type in (TransactionType.BUY, TransactionType.SHORT_SELL))

    def __str__(self) -> str:
        return f"({str(self.transaction_type)} {str(self.equity)}: {self.units} shares for {self.cost} on {str(self.transaction_date)})"

from cachetools import cached, TTLCache
from decimal import Decimal
from enum import Enum
from forex_python.converter import CurrencyRates
from typing import Annotated, Any, Self
from pydantic import BaseModel, BeforeValidator, ConfigDict, model_validator

from . import decimal_from_numeral


class Currency(str, Enum):
    USD = "USD"
    CAD = "CAD"
    EUR = "EUR"
    GBP = "GBP"

    def __str__(self) -> str:
        return self.value

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
    value: Annotated[Decimal, BeforeValidator(lambda value: decimal_from_numeral(value))]
    currency: Currency


    @classmethod
    @cached(cache=TTLCache(maxsize=100, ttl=3600))
    def exchange_rate(cls, 
                      from_currency: Currency, 
                      to_currency: Currency) -> Any:
        """
            Interface for retrieving currency exchange rates. The rates are
            cached for an hour to minimize server class. Should return Decimal
        """
        return CurrencyRates(force_decimal=True).get_rate(from_currency, to_currency)

    @model_validator(mode='after')
    def _is_currency_valid(self) -> Self:
        if(self.currency not in Currency):
            raise ValueError(f"Unrecognized currency: {self.currency}")
        return self

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

    def __add__(self,other:Money) -> Money:
        if(self.currency == other.currency):
            return Money(value=(self.value + other.value), 
                         currency=self.currency)
        else:
            return self + other.convert(target=self.currency)

    def __sub__(self,other:Money) -> Money:
        return self + (-other)

    def __mul__(self, other:(Decimal|int|float)) -> Money:
        other_val = other if(isinstance(other, Decimal)) else decimal_from_numeral(other)
        return Money(value=(self.value*other_val), currency=self.currency)

    def __rmul__(self, other:(Decimal|int|float)) -> Money:
        return self * other

    def __neg__(self):
        return self*-1

    def convert(self, target:Currency) -> Money:
        if(self.currency == target):
            return Money(value=self.value, currency=target)
        rate = self.exchange_rate(self.currency, target)
        return Money(value=(self.value*rate),currency=target)




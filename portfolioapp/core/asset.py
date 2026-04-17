from enum import Enum
from typing import ClassVar, Self
from pydantic import BaseModel, ConfigDict, Field, model_validator


def fake_forex(from_cur:Currency, to_cur:Currency) -> float:
    return 1.5

class Currency(str, Enum):
    USD = "USD"
    CAD = "CAD"
    EUR = "EUR"

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
    value: int | float
    currency: Currency

    # When the exchange rate is retrieved for a pair of currencies for the
    # first time, this dict caches it
    exchange_rates: ClassVar[dict[str, float]] = dict()

    @classmethod
    def exchange_rate(cls, 
                      from_currency: Currency, 
                      to_currency: Currency) -> float:
        if(key:=f"{from_currency}{to_currency}") not in cls.exchange_rates.keys():
            rate =fake_forex(from_currency, to_currency)
            cls.exchange_rates[key] = rate
            cls.exchange_rates[f"{to_currency}{from_currency}"] = 1 / rate
        return cls.exchange_rates[key]


    @model_validator(mode='before')
    @classmethod
    def _value_float_to_int(cls, data: dict) -> dict:
        """ Converts the float value into the internal int representation. """
        if(isinstance(value := data["value"], float)):
            data["value"] = int(value*10000)
        return data

    @model_validator(mode='after')
    def _is_currency_valid(self) -> Self:
        if(self.currency not in Currency):
            raise ValueError(f"Unrecognized currency: {self.currency}")
        return self

    @property
    def _float_value(self):
        return self.value / 10000.0

    def __str__(self) -> str:
        match self.currency:
            case Currency.USD:
                symbol = "$"
            case Currency.CAD:
                symbol = "C$"
            case Currency.EUR:
                symbol = "€"
        return f"{symbol}{self._float_value:.2f}"
    
    def __repr__(self) -> str:
        return f"Money({self._float_value},{str(self.currency)})"

    def __add__(self,other:Money) -> Money:
        if(self.currency == other.currency):
            return Money(value=(self._float_value + other._float_value), 
                         currency=self.currency)
        else:
            return self + other.convert(target=self.currency)

    def __sub__(self,other:Money) -> Money:
        return self + (-1*other)

    def __mul__(self, other:(int|float)) -> Money:
        return Money(value=self.value*other, currency=self.currency)

    def __rmul__(self, other:(int|float)) -> Money:
        return self * other

    def convert(self, target:Currency) -> Money:
        if(self.currency == target):
            return Money(value=self.value, currency=target)
        rate = self.exchange_rate(self.currency, target)
        return Money(value=(self._float_value*rate),currency=target)

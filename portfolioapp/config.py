from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    # The resolution is 0.0001 of the currency
    decimal_precision: int = 4

    # Default values for optional parameters
    default_currency: str = "USD"
    default_exchange: str = "NYSE"
    default_time_format: str = "%m.%d.%y"

    # Imports from .env file
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    MCCI_API_URL: str = Field(alias="MCCI_API_URL")
    MCCI_API_KEY: str = Field(alias="MCCI_API_KEY")
    DB_URL: str = Field(alias="DB_URL")
    CACHE_TTL: int = Field(alias="CACHE_TTL")
    USER_AGENT: str = Field(alias="USER_AGENT")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

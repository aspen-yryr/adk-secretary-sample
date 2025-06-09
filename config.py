from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr


class Config(BaseSettings):
    api_key: SecretStr = Field(default=SecretStr(""))
    model: str = Field(default="openai/gpt-4o-2024-08-06")


config = Config()

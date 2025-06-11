from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    api_key: SecretStr = Field(default=SecretStr(""))
    model: str = Field(default="openai/gpt-4o-2024-08-06")
    openapi_schema_base_dir: str = Field(default="")


config = Config()

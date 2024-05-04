from typing import Tuple, Type

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)


class TelegramSettings(BaseModel):
    token: str
    approval_code: str
    set_commands: bool


class OpenRouterSettings(BaseModel):
    token: str
    default_model: str


class DatabaseSettings(BaseModel):
    connection_string: str


class Settings(BaseSettings):
    telegram: TelegramSettings
    open_router: OpenRouterSettings
    database: DatabaseSettings

    model_config = SettingsConfigDict(toml_file="config.toml")

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)

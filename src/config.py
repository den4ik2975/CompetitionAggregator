from typing import Tuple, Type, List

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)


class EncryptionSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class FastAPISettings(BaseSettings):
    origins: List[str]


class STMPSettings(BaseSettings):
    server: str
    name: str
    password: str
    port: int


class DatabaseSettings(BaseModel):
    connection_string: str


class RedisSettings(BaseModel):
    broker_url: str


class Settings(BaseSettings):
    encryption: EncryptionSettings
    stmp: STMPSettings
    fastapi: FastAPISettings
    database: DatabaseSettings
    redis: RedisSettings

    model_config = SettingsConfigDict(toml_file='config.toml')

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

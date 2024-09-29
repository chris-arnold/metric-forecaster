import os

from pydantic_settings import BaseSettings, SettingsConfigDict


env_file = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".env"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, env_file_encoding='utf-8')
    database_host: str
    database_port: str
    database_user: str
    database_password: str
    database_name: str


settings = Settings()
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, RedisDsn

class Settings(BaseSettings):
    POSTGRES_DSN: PostgresDsn
    REDIS_URL: RedisDsn
    SELENIUM_HOST: str = "selenium"
    SELENIUM_PORT: int = 4444

    PROJECT_NAME: str = "Higher School of Parsing"
    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
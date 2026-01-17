from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    source_url: str = ""
    timeout_seconds: int = 30


settings = Settings()


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения."""
    app_title: str
    database_url: str
    secret: str
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()

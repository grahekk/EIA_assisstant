from pydantic_settings import BaseSettings
from dotenv_settings import port, host, username, password, db_name


class LocalSettings(BaseSettings):
    env_name: str = "Local"
    port: int = port
    host: str = host
    username: str = username
    db_name: str = db_name
    password: str = password
    database_url: str = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"

    class Config:
        env_file = ".env"

class Settings(BaseSettings):
    local: LocalSettings
    env_name: str = "Local"
    database_url = LocalSettings.database_url

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings


settings = get_settings()
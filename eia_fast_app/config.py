from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./eia_app.db"

    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings


# get_settings().db_url
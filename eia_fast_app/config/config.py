from pydantic_settings import BaseSettings
from .dotenv_settings import port, host, user, password, db_name

config_args = {"host": host,
               "user": user, 
               "port": port,
                "password": password,
                "dbname": db_name
}

database_url: str = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

# class LocalSettings(BaseSettings):
#     env_name: str = "Local"
#     port: int
#     host: str
#     username: str
#     db_name: str
#     password: str

#     @property
#     def database_url(self):
#         return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"

#     class Config:
#         env_file = ".env"

# class Settings(BaseSettings):
#     local: LocalSettings
#     env_name: str = "Local"

#     @property
#     def database_url(self):
#         return self.local.database_url

#     class Config:
#         env_file = ".env"


# def get_settings() -> Settings:
#     settings = Settings()
#     print(f"Loading settings for: {settings.env_name}")
#     return settings


# settings = get_settings()
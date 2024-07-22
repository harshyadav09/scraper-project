from pydantic import BaseSettings

class Settings(BaseSettings):
    AUTH_TOKEN: str = "your_static_token"

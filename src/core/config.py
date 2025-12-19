from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    
    class Config:
        env_file = ".env" # Указываем путь к файлу
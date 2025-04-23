from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Sube una carpeta

class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSGRES_PORT: str
    JWT_SECRET: str
    JWT_ALGORITHM: str

    POSTGRES_HOST_EXTERNAL: str
    POSTGRES_USER_EXTERNAL: str
    POSTGRES_PASSWORD_EXTERNAL: str
    POSTGRES_DB_EXTERNAL: str
    POSTGRES_PORT_EXTERNAL: str
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )

Config = Settings()

def create_db_url():
    url = f"postgresql+asyncpg://{Config.POSTGRES_USER}:{Config.POSTGRES_PASSWORD}@{Config.POSTGRES_HOST}:{Config.POSGRES_PORT}/{Config.POSTGRES_DB}"
    return url
   
def create_db_url_external():
    url = f"postgresql+asyncpg://{Config.POSTGRES_USER_EXTERNAL}:{Config.POSTGRES_PASSWORD_EXTERNAL}@{Config.POSTGRES_HOST_EXTERNAL}:{Config.POSTGRES_PORT_EXTERNAL}/{Config.POSTGRES_DB_EXTERNAL}"
    return url
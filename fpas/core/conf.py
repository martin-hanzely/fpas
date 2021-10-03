from typing import TYPE_CHECKING

from pydantic import BaseSettings

# avoid mypy type error with litteral string assignment
if TYPE_CHECKING:
    AnyHttpUrl = str
    PostgresDsn = str
else:
    from pydantic import AnyHttpUrl, PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = "fpas"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    SERVER_HOST: AnyHttpUrl = "http://localhost:8000"
    SECRET_KEY: str = "development"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []  # JSON-formatted list
    POSTGRES_DSN: PostgresDsn = f"postgresql://postgres:postgres@localhost:5432/{PROJECT_NAME}_dev"

    class Config:
        case_sensitive = True


settings = Settings()

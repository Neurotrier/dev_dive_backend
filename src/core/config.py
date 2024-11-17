import os
import tomllib
from pathlib import Path

from dotenv import load_dotenv
from pydantic import computed_field
from pydantic_settings import BaseSettings

load_dotenv()
BASE_DIR = Path(__file__).parent.parent.parent
with open(BASE_DIR / "pyproject.toml", "rb") as f:
    pyproject_data = tomllib.load(f)
    project_version = pyproject_data["project"]["version"]
    project_name = pyproject_data["project"]["name"]
    project_description = pyproject_data["project"]["description"]
    project_author = pyproject_data["project"]["authors"][0]


class Settings(BaseSettings):
    """App config settings"""

    PROJECT_NAME: str = project_name
    PROJECT_VERSION: str = project_version
    PROJECT_DESCRIPTION: str = project_description
    PROJECT_AUTHOR: str = project_author

    UPVOTE_VALUE: int = os.getenv("UPVOTE_VALUE")
    DOWNVOTE_VALUE: int = os.getenv("DOWNVOTE_VALUE")
    BAN_THRESHOLD: int = os.getenv("BAN_THRESHOLD")
    MODERATOR_THRESHOLD: int = os.getenv("MODERATOR_THRESHOLD")

    DEBUG: bool = os.getenv("DEBUG", False)

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")

    access_token_ttl_min: int = os.getenv("ACCESS_TOKEN_TTL_MIN")
    refresh_token_ttl_min: int = os.getenv("REFRESH_TOKEN_TTL_MIN")
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    token_type: str = "Bearer"
    algorithm: str = "HS256"

    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    CACHE_NAME: str = os.getenv("CACHE_NAME")

    MINIO_HOST: str = os.getenv("MINIO_HOST")
    MINIO_PORT: int = os.getenv("MINIO_PORT")
    ACCESS_KEY: str = os.getenv("ACCESS_KEY")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    BUCKET_NAME: str = os.getenv("BUCKET_NAME")

    @computed_field
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @computed_field
    @property
    def SYNC_DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @computed_field
    @property
    def MINIO_URL(self) -> str:
        return f"{self.MINIO_HOST}:{self.MINIO_PORT}"

    @computed_field
    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:" f"{self.REDIS_PORT}/1"


settings = Settings()

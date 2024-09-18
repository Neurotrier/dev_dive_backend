import os
from pathlib import Path

import tomllib
from dotenv import load_dotenv
from pydantic import computed_field
from pydantic_settings import BaseSettings

load_dotenv()
BASE_DIR = Path(__file__).parent.parent.parent
with open(BASE_DIR / "pyproject.toml", "rb") as f:
    pyproject_data = tomllib.load(f)
    project_version = pyproject_data["tool"]["poetry"]["version"]
    project_name = pyproject_data["tool"]["poetry"]["name"]
    project_description = pyproject_data["tool"]["poetry"]["description"]
    project_author = pyproject_data["tool"]["poetry"]["authors"][0]


class Settings(BaseSettings):
    """App config settings"""

    PROJECT_NAME: str = project_name
    PROJECT_VERSION: str = project_version
    PROJECT_DESCRIPTION: str = project_description
    PROJECT_AUTHOR: str = project_author

    DEBUG: bool = os.getenv("DEBUG", False)

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


settings = Settings()

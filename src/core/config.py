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

    DATABASE_HOST: str = os.getenv("DATABASE_HOST")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT")
    DATABASE_USER: str = os.getenv("DATABASE_USER")

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@"
            f"{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/"
            f"{self.DATABASE_NAME}"
        )


settings = Settings()

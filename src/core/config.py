from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Setting(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///db.sqlite3"
    db_echo: bool = False


settings = Setting()



import re

from fastapi import HTTPException
from starlette import status

from src.core.role import Role


def check_email(email: str) -> str:
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-]+\.[a-zA-Z0-9-]+$"
    if re.match(email_pattern, email) is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid email format!"
        )
    return email


def check_password(password: str) -> str:
    forbidden_symbols = [ord(i) for i in ("\\", "/", "$", "@", "%", "&")]
    for symbol in password:
        if ord(symbol) in forbidden_symbols:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Forbidden symbols in password!",
            )
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="The length of your password should be at least 8 characters!",
        )
    return password


def check_username(username: str) -> str:
    if len(username) > 30:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="The length of your username should be at most 30 characters!",
        )
    return username


def check_role(role: Role) -> Role:
    if role == Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Policy denied",
        )
    return role

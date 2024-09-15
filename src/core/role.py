import enum


class Role(enum.StrEnum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

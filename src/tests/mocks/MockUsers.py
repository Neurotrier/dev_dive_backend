from src.core.role import Role

mock_users = {
    "1": {
        "username": "bob",
        "id": "1",
        "info": None,
        "image_url": None,
        "is_banned": False,
        "reputation": 100,
        "role": Role.MODERATOR,
    },
    "2": {
        "username": "tot",
        "id": "2",
        "info": "Hello world",
        "image_url": None,
        "is_banned": True,
        "reputation": -3400,
        "role": Role.USER,
    },
}

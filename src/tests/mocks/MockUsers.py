from src.core.role import Role

mock_users = {
    "4b6a57ef-0105-484f-afd8-4f7f3c08cf7e": {
        "username": "bob",
        "id": "4b6a57ef-0105-484f-afd8-4f7f3c08cf7e",
        "info": None,
        "image_url": None,
        "is_banned": False,
        "reputation": 100,
        "role": Role.MODERATOR,
    },
    "a2319134-5801-43c0-bd21-5c62f901f33c": {
        "username": "tot",
        "id": "a2319134-5801-43c0-bd21-5c62f901f33c",
        "info": "Hello world",
        "image_url": None,
        "is_banned": True,
        "reputation": -3400,
        "role": Role.USER,
    },
}

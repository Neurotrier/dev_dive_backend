class MockUserRepository:
    def __init__(self):
        self.users = {"1": {"username": "bob", "id": "1", 'info': None, 'image_url': None}}
        self.committed = False
        self.rolled_back = False

    async def get_user(self, user_id):
        return self.users.get(user_id)

    async def update(self, data, id):
        print(data)
        if id in self.users:
            user = self.users.get(id)
            user.update(data)
            return user

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True


class MockUserRepository:
    def __init__(self, users):
        self.users = users
        self.committed = False
        self.rolled_back = False

    async def get_by_pk(self, id):
        return self.users.get(id)

    async def update(self, data, id):
        id = str(id)
        if id in self.users:
            user = self.users.get(id)
            user.update(data)
            return user

    async def delete_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            return user_id
        return None

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True

    @staticmethod
    def to_schema(user):
        return user

# database/users_chats_db.py

from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI

class MongoDB:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_DB_URI)
        self.db = self.client["autofilter_db"]
        self.users = self.db.users
        self.chats = self.db.chats

    async def add_user(self, user_id: int, name: str = ""):
        user = await self.users.find_one({"user_id": user_id})
        if not user:
            await self.users.insert_one({"user_id": user_id, "name": name})

    async def get_all_users(self):
        return self.users.find()

    async def add_chat(self, chat_id: int, title: str = ""):
        chat = await self.chats.find_one({"chat_id": chat_id})
        if not chat:
            await self.chats.insert_one({"chat_id": chat_id, "title": title})

    async def get_all_chats(self):
        return self.chats.find()

    async def is_user_exist(self, user_id: int) -> bool:
        return await self.users.find_one({"user_id": user_id}) is not None

    async def is_chat_exist(self, chat_id: int) -> bool:
        return await self.chats.find_one({"chat_id": chat_id}) is not None

    async def remove_user(self, user_id: int):
        await self.users.delete_one({"user_id": user_id})

    async def remove_chat(self, chat_id: int):
        await self.chats.delete_one({"chat_id": chat_id})


# Global database instance
db = MongoDB()

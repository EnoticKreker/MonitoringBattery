from repositories.base import BaseRepository
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.get(email=email)

    async def create_user(self, email: str, password: str, role: str = "USER"):
        obj = User(email=email, password=password, role=role)
        self.session.add(obj)
        await self.session.commit()
        return obj

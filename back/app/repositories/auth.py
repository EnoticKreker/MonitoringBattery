from repositories.base import BaseRepository
from models.refresh_token import RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: AsyncSession):
        super().__init__(RefreshToken, session)

    async def add_refresh(self, user_id: int, refresh_token: str) -> Optional[RefreshToken]:
        obj = RefreshToken(user_id=user_id, token=refresh_token)
        self.session.add(obj)
        await self.session.commit()
        return obj

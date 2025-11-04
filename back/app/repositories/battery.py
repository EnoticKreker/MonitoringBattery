from repositories.base import BaseRepository
from models.battery import Battery
from sqlalchemy.ext.asyncio import AsyncSession


class BatteryRepository(BaseRepository[Battery]):
    def __init__(self, session: AsyncSession):
        super().__init__(Battery, session)

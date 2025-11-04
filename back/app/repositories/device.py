from repositories.base import BaseRepository
from models.device import Device
from sqlalchemy.ext.asyncio import AsyncSession


class DeviceRepository(BaseRepository[Device]):
    def __init__(self, session: AsyncSession):
        super().__init__(Device, session)

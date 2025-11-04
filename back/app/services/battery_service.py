from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.battery import BatteryRepository
from repositories.device import DeviceRepository
from models.battery import Battery
from schemas.battery import BatteryCreate, BatteryUpdate


class BatteryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = BatteryRepository(session)
        self.device_repo = DeviceRepository(session)

    async def create_battery(self, battery_in: BatteryCreate) -> Battery:
        if battery_in.device_id is not None:
            device = await self.device_repo.get_by_id(battery_in.device_id)
            if not device:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Device with id={battery_in.device_id} does not exist"
                )
        data = battery_in.model_dump()

        try:
            battery = await self.repo.create(data)
            await self.session.commit()
            return battery
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error while create battery: {str(e)}",
            )

    async def update_battery(self, battery: Battery, update_in: BatteryUpdate) -> Battery:
        update_data = update_in.model_dump(exclude_none=True)
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No fields provided for update"
            )

        if "device_id" in update_data:
            device = await self.device_repo.get_by_id(update_data["device_id"])
            if not device:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Device with id={update_data['device_id']} does not exist"
                )

        if "device_id" in update_in.model_dump():
            update_data["device_id"] = update_in.device_id

        try:
            battery = await self.repo.update(battery, update_data)
            await self.session.commit()
            await self.session.refresh(battery)
            return battery
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error while updating post: {str(e)}",
            )

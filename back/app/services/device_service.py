from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.battery import BatteryRepository
from repositories.device import DeviceRepository
from models.device import Device
from schemas.device import DeviceCreate, DeviceUpdate


class DeviceService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = DeviceRepository(session)
        self.repoBatt = BatteryRepository(session)

    async def create_device(self, device_in: DeviceCreate) -> Device:
        find_name = await self.repo.get(name=device_in.name)
        if find_name:
            raise HTTPException(status_code=400, detail="Name already exists")
        data = device_in.model_dump(exclude_unset=True)
        batteries_data = data.pop("batteries", None)

        try:
            device = await self.repo.create(data)
            if batteries_data:
                device = await self.add_battareies_to_device(device, batteries_data)

            await self.session.commit()
            await self.session.refresh(device, attribute_names=["batteries"])
            return device
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error while create device: {str(e)}",
            )

    async def update_device(self, device: Device, update_in: DeviceUpdate) -> Device:
        update_data = update_in.model_dump(exclude_none=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"No data provided to update"
            )

        if "name" in update_data and update_data["name"] != device.name:
            name_device = await self.repo.get(name=update_data['name'])
            if name_device:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Device with name={update_data['name']} already exists"
                )

        batteries_data = update_data.pop("batteries", None)

        try:
            device = await self.repo.update(device, update_data)

            if batteries_data:
                device = await self.add_battareies_to_device(device, batteries_data)

            await self.session.commit()
            await self.session.refresh(device)
            return device
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error while updating category: {str(e)}",
            )

    async def add_bat_to_dev(self, device: Device, battareies_data: list[dict]) -> Device:
        device = await self.add_battareies_to_device(device, battareies_data)
        await self.session.commit()
        await self.session.refresh(device, attribute_names=["batteries"])
        return device

    async def add_battareies_to_device(self, device: Device, battareies_data: list[dict]) -> Device:
        dev = await self.repo.get_by_id(device.id)
        current_bat = len(dev.batteries)
        new_bat = len(battareies_data)

        if current_bat + new_bat > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Device can have maximum 5 batteries. Currently has {current_bat}, tried to add {new_bat}"
            )

        for b in battareies_data:
            if "id" in b:
                battery = await self.repoBatt.get_by_id(b["id"])
                if not battery:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Battery with id={b['id']} not found"
                    )
            else:
                battery = await self.repoBatt.create(b)

            device.batteries.append(battery)
        try:
            await self.session.flush()
            return device
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error while adding batteries: {str(e)}"
            )

    async def remove_battery_from_device(self, device_id: int, battery_id: int) -> Device:
        device = await self.repo.get_by_id(device_id)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Device with id={device_id} not found"
            )

        battery = await self.repoBatt.get_by_id(battery_id)
        if not battery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Battery with id={battery_id} not found"
            )

        if battery not in device.batteries:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Battery id={battery_id} is not attached to device id={device_id}"
            )

        try:
            device.batteries.remove(battery)
            await self.session.commit()
            await self.session.refresh(device, attribute_names=["batteries"])
            return device
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error while removing battery: {str(e)}"
            )

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.battery import BatteryAddToDevice
from core.database import get_session
from services.device_service import DeviceService
from repositories.device import DeviceRepository
from schemas.device import DeviceCreate, DeviceRead, DeviceUpdate
from auth.dependencies import admin_required

router = APIRouter(prefix="/api/v1/devices", tags=["devices"])


@router.get("", response_model=list[DeviceRead])
async def list_devices(offset: int = 0, limit: int = 20, session: AsyncSession = Depends(get_session)):
    repo = DeviceRepository(session)
    dev = await repo.list(offset=offset, limit=limit)
    return dev


@router.get("/{device_id}", response_model=DeviceRead)
async def get_device(device_id: str, session: AsyncSession = Depends(get_session)):
    repo = DeviceRepository(session)
    device = await repo.get_by_id(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("", response_model=DeviceRead, dependencies=[Depends(admin_required)])
async def create_device(payload: DeviceCreate, session: AsyncSession = Depends(get_session)):
    service = DeviceService(session)
    device = await service.create_device(payload)
    return device


@router.put("/{device_id}", response_model=DeviceRead, dependencies=[Depends(admin_required)])
async def update_device(device_id: int, payload: DeviceUpdate, session: AsyncSession = Depends(get_session)):
    repo = DeviceRepository(session)
    device = await repo.get_by_id(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    service = DeviceService(session)
    updated = await service.update_device(device, payload)
    return updated


@router.delete("/{device_id}", status_code=204, dependencies=[Depends(admin_required)])
async def delete_category(device_id: int, session: AsyncSession = Depends(get_session)):
    repo = DeviceRepository(session)
    device = await repo.get_by_id(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    await repo.delete(device)
    await session.commit()
    return None


@router.post("/{device_id}/battaries", response_model=DeviceRead)
async def add_battaries(device_id: int, battaries: list[BatteryAddToDevice], session: AsyncSession = Depends(get_session)):
    device_repo = DeviceRepository(session)

    device = await device_repo.get_by_id(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    service = DeviceService(session)
    updated_device = await service.add_bat_to_dev(device, [b.model_dump(exclude_unset=True) for b in battaries])
    return updated_device


@router.delete("/{device_id}/battaries/{battery_id}", response_model=DeviceRead)
async def delete_battery_by_device(device_id: int, battery_id: int, session: AsyncSession = Depends(get_session)):
    service = DeviceService(session)
    return await service.remove_battery_from_device(device_id, battery_id)

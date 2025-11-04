from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from repositories.battery import BatteryRepository
from auth.dependencies import admin_required
from schemas.battery import BatteryCreate, BatteryRead, BatteryUpdate
from services.battery_service import BatteryService
from typing import List

router = APIRouter(prefix="/api/v1/battery", tags=["battery"])


@router.get("", response_model=List[BatteryRead])
async def list_batteries(offset: int = 0, limit: int = 20, session: AsyncSession = Depends(get_session)):
    repo = BatteryRepository(session)
    batteries = await repo.list(offset=offset, limit=limit)
    return batteries


@router.get("/{id}", response_model=BatteryRead)
async def get_battery(id: str, session: AsyncSession = Depends(get_session)):
    repo = BatteryRepository(session)
    battery = await repo.get_by_id(id)
    if not battery:
        raise HTTPException(status_code=404, detail="Battery not found")
    return battery


@router.post("", response_model=BatteryRead, dependencies=[Depends(admin_required)])
async def create_battery(payload: BatteryCreate, session: AsyncSession = Depends(get_session)):
    service = BatteryService(session)
    battery = await service.create_battery(payload)
    return battery


@router.put("/{battery_id}", response_model=BatteryRead, dependencies=[Depends(admin_required)])
async def update_battery(battery_id: int, payload: BatteryUpdate, session: AsyncSession = Depends(get_session)):
    repo = BatteryRepository(session)
    battery = await repo.get_by_id(battery_id)
    if not battery:
        raise HTTPException(status_code=404, detail="Battery not found")
    service = BatteryService(session)
    updated = await service.update_battery(battery, payload)
    return updated


@router.delete("/{battery_id}", status_code=204, dependencies=[Depends(admin_required)])
async def delete_battery(battery_id: int, session: AsyncSession = Depends(get_session)):
    repo = BatteryRepository(session)
    battery = await repo.get_by_id(battery_id)
    if not battery:
        raise HTTPException(status_code=404, detail="Battery not found")
    await repo.delete(battery)
    await session.commit()
    return None

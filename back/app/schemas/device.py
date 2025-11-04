from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from schemas.battery import BatteryAddToDevice, BatteryRead


class DeviceBase(BaseModel):
    name: str
    version: str
    status: bool = False


class DeviceCreate(DeviceBase):
    batteries: Optional[List[BatteryAddToDevice]] = None


class DeviceUpdate(BaseModel):
    name: str = None
    version: str = None
    status: bool = None
    batteries: Optional[List[BatteryAddToDevice]] = None


class DeviceRead(DeviceBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    batteries: Optional[List[BatteryRead]] = None

    model_config = ConfigDict(from_attributes=True)

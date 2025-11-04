from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class BatteryBase(BaseModel):
    name: str = Field(..., max_length=300)
    voltage: str
    residual_capacity: str
    lifetime: str
    device_id: Optional[int] = None


class BatteryCreate(BatteryBase):
    pass


class BatteryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=300)
    voltage: Optional[str] = None
    residual_capacity: Optional[str] = None
    lifetime: Optional[str] = None
    device_id: Optional[int] = None


class BatteryAddToDevice(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = Field(None, max_length=300)
    voltage: Optional[str] = None
    residual_capacity: Optional[str] = None
    lifetime: Optional[str] = None


class BatteryRead(BatteryBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

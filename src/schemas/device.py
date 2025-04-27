from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    name: str
    serial_number: str

class DeviceCreate(DeviceBase):
    user_id: int

class DeviceUpdate(DeviceBase):
    pass

class DeviceInDB(DeviceBase):
    id: str
    user_id: int
    api_key: str
    created_at: datetime
    last_seen: Optional[datetime] = None
    
    class Config:
        from_attributes = True 
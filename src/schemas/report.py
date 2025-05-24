import json
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List
from datetime import datetime

class Host(BaseModel):
    ip: str
    status: str
    ports: List[int]
    services: List[str]
    time: datetime

class ReportData(BaseModel):
    hosts: List[Host]

class ReportBase(BaseModel):
    device_id: str
    location: Optional[str] = None
    data: ReportData

class ReportCreate(ReportBase):
    pass

class ReportInDB(BaseModel):
    id: str
    user_id: int
    device_id: str
    location: Optional[str] = None
    data: ReportData
    created_at: datetime

    @field_validator("data", mode="before")
    @classmethod
    def validate_data(cls, v):
        if isinstance(v, str):
            try:
                return ReportData.model_validate_json(v)
            except Exception:
                return ReportData(hosts=[])
        return v if isinstance(v, ReportData) else ReportData(hosts=[])

    class Config:
        from_attributes = True
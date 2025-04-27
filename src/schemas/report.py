import json
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List
from datetime import datetime

class ReportBase(BaseModel):
    device_id: str
    location: Optional[str] = None
    data: List[Dict[str, Any]]

class ReportCreate(ReportBase):
    pass

class ReportInDB(BaseModel):
    id: str
    user_id: int
    device_id: str
    location: Optional[str] = None
    data: List[Dict[str, Any]]
    created_at: datetime

    @field_validator("data", mode="before")
    @classmethod
    def validate_data(cls, v):
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                return parsed if isinstance(parsed, list) else [parsed] if parsed else []
            except json.JSONDecodeError:
                return []
        return v if isinstance(v, list) else []

    class Config:
        from_attributes = True
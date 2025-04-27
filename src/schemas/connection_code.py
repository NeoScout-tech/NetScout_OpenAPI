from pydantic import BaseModel
from datetime import datetime

class ConnectionCodeBase(BaseModel):
    code: str

class ConnectionCodeCreate(ConnectionCodeBase):
    expires_at: datetime

class ConnectionCodeInDB(ConnectionCodeBase):
    id: int
    user_id: int
    expires_at: datetime
    
    class Config:
        from_attributes = True 
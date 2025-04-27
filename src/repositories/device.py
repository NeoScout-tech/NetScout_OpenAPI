from typing import Optional, List
from sqlalchemy.orm import Session
from src.models.device import Device
from src.repositories.base import BaseRepository

class DeviceRepository(BaseRepository[Device]):
    def get_by_api_key(self, db: Session, api_key: str) -> Optional[Device]:
        return db.query(Device).filter(Device.api_key == api_key).first()
    
    def get_by_user_id(self, db: Session, user_id: int) -> List[Device]:
        return db.query(Device).filter(Device.user_id == user_id).all()
    
    def get_by_serial_number(self, db: Session, serial_number: str) -> Optional[Device]:
        return db.query(Device).filter(Device.serial_number == serial_number).first() 
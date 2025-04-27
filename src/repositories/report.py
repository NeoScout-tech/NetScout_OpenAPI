from typing import Optional, List
from sqlalchemy.orm import Session
from src.models.report import Report
from src.repositories.base import BaseRepository

class ReportRepository(BaseRepository[Report]):
    def get_by_user_id(self, db: Session, user_id: int) -> List[Report]:
        return db.query(Report).filter(Report.user_id == user_id).all()
    
    def get_by_device_id(self, db: Session, device_id: str) -> List[Report]:
        return db.query(Report).filter(Report.device_id == device_id).all()
    
    def get_by_user_and_device(self, db: Session, user_id: int, device_id: str) -> List[Report]:
        return db.query(Report).filter(
            Report.user_id == user_id,
            Report.device_id == device_id
        ).all() 
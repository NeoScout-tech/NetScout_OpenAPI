from typing import Optional
from sqlalchemy.orm import Session
from src.models.connection_code import ConnectionCode
from src.repositories.base import BaseRepository

class ConnectionCodeRepository(BaseRepository[ConnectionCode]):
    def get_by_code(self, db: Session, code: str) -> Optional[ConnectionCode]:
        return db.query(ConnectionCode).filter(ConnectionCode.code == code).first() 
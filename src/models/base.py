from datetime import datetime
from sqlalchemy import Column, DateTime
from src.database.config import Base

class BaseModel(Base):
    __abstract__ = True
    
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            **{c.name: getattr(self, c.name) for c in self.__table__.columns},
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 
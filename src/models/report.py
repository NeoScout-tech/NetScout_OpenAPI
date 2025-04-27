from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from src.models.base import Base
import uuid
import json
from datetime import datetime

class Report(Base):
    __tablename__ = "report"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    device_id = Column(String(32), ForeignKey("device.id"), nullable=False)
    location = Column(String(255))
    data = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reports")
    device = relationship("Device", back_populates="reports")

    def __repr__(self):
        return f"<Report {self.id}>"

    @property
    def data_dict(self):
        if isinstance(self.data, str):
            try:
                data = json.loads(self.data)
                return data if isinstance(data, list) else [data] if data else []
            except json.JSONDecodeError:
                return []
        return self.data if isinstance(self.data, list) else []

    def to_dict(self):
        return {
            **{c.name: getattr(self, c.name) for c in self.__table__.columns},
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "data": self.data_dict
        }
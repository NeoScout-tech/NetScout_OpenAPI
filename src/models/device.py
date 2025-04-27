from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.models.base import Base
import uuid
from datetime import datetime

class Device(Base):
    __tablename__ = "device"

    id = Column(String(32), primary_key=True, default=lambda: str(uuid.uuid4()).replace('-', ''))
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    api_key = Column(String(32), unique=True, nullable=False)
    serial_number = Column(String(80))
    last_seen = Column(DateTime)

    user = relationship("User", back_populates="devices")
    reports = relationship("Report", back_populates="device")

    def __repr__(self):
        return f"<Device {self.name}>" 
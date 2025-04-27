from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.models.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128))
    telegram = Column(String(80))

    devices = relationship("Device", back_populates="user")
    reports = relationship("Report", back_populates="user")
    api_keys = relationship("ApiKey", back_populates="user")
    contact_messages = relationship("ContactMessage", back_populates="user")
    connection_codes = relationship("ConnectionCode", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>" 
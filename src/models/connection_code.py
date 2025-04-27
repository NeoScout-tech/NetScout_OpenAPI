from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database.config import Base

class ConnectionCode(Base):
    __tablename__ = 'connection_code'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    code = Column(String(6), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    
    user = relationship('User', back_populates='connection_codes')
    
    def __repr__(self):
        return f"<ConnectionCode {self.code}>" 
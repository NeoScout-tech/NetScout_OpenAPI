from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class ApiKey(BaseModel):
    __tablename__ = 'api_key'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    key = Column(String(32), unique=True, nullable=False)
    
    user = relationship('User', back_populates='api_keys')
    
    def __repr__(self):
        return f"<ApiKey {self.key[:8]}...>" 
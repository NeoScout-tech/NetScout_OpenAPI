from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class ContactMessage(BaseModel):
    __tablename__ = 'contact_message'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    subject = Column(String(120), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    
    user = relationship('User', back_populates='contact_messages')
    
    def __repr__(self):
        return f"<ContactMessage {self.subject}>" 
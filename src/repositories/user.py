from typing import Optional
from sqlalchemy.orm import Session
from src.models.user import User
from src.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()
    
    def get_by_api_key(self, db: Session, api_key: str) -> Optional[User]:
        return db.query(User).join(User.api_keys).filter(User.api_keys.any(key=api_key)).first() 
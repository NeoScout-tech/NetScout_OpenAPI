from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.repositories.user import UserRepository
from src.schemas.user import UserInDB
from src.models.user import User

security = HTTPBearer()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(security)]
)

user_repo = UserRepository(User)

@router.get("/me", response_model=UserInDB)
def get_me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Получает информацию о текущем пользователе.
    
    Args:
        credentials: Данные авторизации
        db: Сессия базы данных
        
    Returns:
        UserInDB: Информация о пользователе
    """
    user = user_repo.get_by_api_key(db, credentials.credentials)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database.config import get_db
from src.repositories.user import UserRepository
from src.models.user import User

async def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    Получает текущего пользователя по API ключу из заголовка запроса.
    
    Args:
        request: Запрос FastAPI
        db: Сессия базы данных
        
    Returns:
        User: Объект пользователя
        
    Raises:
        HTTPException: Если API ключ не указан или недействителен
    """
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(status_code=401, detail="API key is required")
    
    user_repo = UserRepository(User)
    user = user_repo.get_by_api_key(db, api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return user

def check_ownership(user_id: int, current_user: User):
    """
    Проверяет, является ли пользователь владельцем ресурса.
    
    Args:
        user_id: ID пользователя-владельца ресурса
        current_user: Текущий пользователь
        
    Raises:
        HTTPException: Если текущий пользователь не является владельцем
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions") 
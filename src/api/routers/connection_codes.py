from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.repositories.connection_code import ConnectionCodeRepository
from src.schemas.connection_code import ConnectionCodeCreate, ConnectionCodeInDB
from src.models.connection_code import ConnectionCode
from src.models.user import User
from src.repositories.user import UserRepository

security = HTTPBearer()

router = APIRouter(
    prefix="/connection-codes",
    tags=["connection-codes"],
    dependencies=[Depends(security)]
)
connection_code_repo = ConnectionCodeRepository(ConnectionCode)

@router.post("/", response_model=ConnectionCodeInDB)
def create_connection_code(
    connection_code: ConnectionCodeCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Создает новый код подключения.
    Доступно только для создания кодов в своем аккаунте.
    
    Args:
        connection_code: Данные для создания кода
        credentials: Данные авторизации
        db: Сессия базы данных
        
    Returns:
        ConnectionCodeInDB: Созданный код подключения
        
    Raises:
        HTTPException: Если нет прав на создание кода
    """
    user = UserRepository(User).get_by_api_key(db, credentials.credentials)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return connection_code_repo.create(db, obj_in=connection_code.model_dump())
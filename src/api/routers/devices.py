from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

from src.database.config import get_db
from src.repositories.device import DeviceRepository
from src.schemas.device import DeviceInDB
from src.models.device import Device
from src.models.user import User
from src.api.middleware.auth import check_ownership
from src.repositories.user import UserRepository

security = HTTPBearer()

router = APIRouter(
    prefix="/devices",
    tags=["Устройства"],
    dependencies=[Depends(security)]
)
device_repo = DeviceRepository(Device)

@router.get("/", response_model=List[DeviceInDB])
def get_devices(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Получение списка устройств текущего пользователя.
    
    Args:
        credentials: Данные авторизации
        db: Сессия базы данных
        
    Returns:
        List[DeviceInDB]: Список устройств пользователя
    """
    user = UserRepository(User).get_by_api_key(db, credentials.credentials)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return device_repo.get_by_user_id(db, user.id)

@router.get("/{device_id}", response_model=DeviceInDB)
def get_device(
    device_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Получение информации об устройстве по ID.
    
    Доступно только для просмотра своих устройств.
    
    Args:
        device_id: ID устройства
        credentials: Данные авторизации
        db: Сессия базы данных
        
    Returns:
        DeviceInDB: Информация об устройстве
        
    Raises:
        HTTPException: Если устройство не найдено или нет прав доступа
    """
    user = UserRepository(User).get_by_api_key(db, credentials.credentials)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    db_device = device_repo.get(db, id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Устройство не найдено")
    check_ownership(db_device.user_id, user)
    return db_device
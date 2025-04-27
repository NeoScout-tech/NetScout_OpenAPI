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
    tags=["devices"],
    dependencies=[Depends(security)]
)
device_repo = DeviceRepository(Device)

@router.get("/", response_model=List[DeviceInDB])
def get_devices(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get list of devices for current user.
    
    Args:
        credentials: Authorization data
        db: Database session
        
    Returns:
        List[DeviceInDB]: List of user devices
    """
    user = UserRepository(User).get_by_api_key(db, credentials.credentials)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return device_repo.get_by_user_id(db, user.id)

@router.get("/{device_id}", response_model=DeviceInDB)
def get_device(
    device_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get device information by ID.
    Available only for viewing own devices.
    
    Args:
        device_id: Device ID
        credentials: Authorization data
        db: Database session
        
    Returns:
        DeviceInDB: Device information
        
    Raises:
        HTTPException: If device not found or no access rights
    """
    user = UserRepository(User).get_by_api_key(db, credentials.credentials)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_device = device_repo.get(db, id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    check_ownership(db_device.user_id, user)
    return db_device
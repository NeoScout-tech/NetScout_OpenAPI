from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
import uuid

from src.database.config import get_db
from src.repositories.report import ReportRepository
from src.schemas.report import ReportCreate, ReportInDB
from src.models.device import Device
from src.models.report import Report
from src.models.user import User
from src.repositories.user import UserRepository
from src.repositories.device import DeviceRepository

security = HTTPBearer()

router = APIRouter(
    prefix="/reports",
    tags=["Отчеты"],
    dependencies=[Depends(security)]
)
report_repo = ReportRepository(Report)
device_repo = DeviceRepository(Device)

def get_or_create_nmap_device(db: Session, user_id: int) -> Device:
    """
    Получение или создание устройства NMAP для пользователя.
    
    Args:
        db: Сессия базы данных
        user_id: ID пользователя
        
    Returns:
        Device: Устройство NMAP
    """
    # Ищем существующее устройство NMAP
    nmap_device = db.query(Device).filter(
        Device.user_id == user_id,
        Device.name == "NMAP"
    ).first()
    
    if not nmap_device:
        # Создаем новое устройство NMAP
        device_data = {
            "id": str(uuid.uuid4()).replace('-', ''),
            "name": "NMAP",
            "user_id": user_id,
            "api_key": str(uuid.uuid4()).replace('-', ''),
            "serial_number": f"NMAP-{user_id}"
        }
        nmap_device = device_repo.create(db, obj_in=device_data)
    
    return nmap_device

@router.post("/", response_model=ReportInDB)
def create_report(
    report: ReportCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Создание нового отчета о сканировании.
    
    Доступно только для создания отчетов от своих устройств.
    Если пользователь использует свой API ключ и имя устройства "NMAP", 
    то устройство будет создано автоматически.
    
    Args:
        report: Данные для создания отчета
            - device_id: ID устройства
            - location: Опциональное местоположение
            - data: Данные отчета в формате:
                ```json
                {
                    "hosts": [
                        {
                            "ip": "192.168.1.10",
                            "status": "active",
                            "ports": [80, 443],
                            "services": ["Apache httpd 2.4.49"],
                            "time": "2024-05-05 10:00:00"
                        }
                    ]
                }
                ```
        credentials: Данные авторизации
        db: Сессия базы данных
        
    Returns:
        ReportInDB: Созданный отчет
        
    Raises:
        HTTPException: Если устройство не найдено или нет прав доступа
    """
    api_key = credentials.credentials
    
    # Сначала проверяем, не пользовательский ли это токен
    user = UserRepository(User).get_by_api_key(db, api_key)
    if user:
        # Если это токен пользователя и имя устройства NMAP - создаем/получаем устройство
        if report.device_id == "NMAP":
            device = get_or_create_nmap_device(db, user.id)
        else:
            raise HTTPException(status_code=403, detail="Используйте API ключ устройства для отправки отчетов")
    else:
        # Если это не токен пользователя, ищем устройство
        device = db.query(Device).filter(Device.api_key == api_key).first()
        if not device:
            raise HTTPException(status_code=404, detail="Устройство не найдено")
    
    report_data = report.model_dump()
    report_data["user_id"] = device.user_id
    return report_repo.create(db, obj_in=report_data)

@router.get("/", response_model=List[ReportInDB])
def get_reports(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Получение списка отчетов текущего пользователя.
    
    Args:
        credentials: Данные авторизации
        db: Сессия базы данных
        
    Returns:
        List[ReportInDB]: Список отчетов пользователя
    """
    user = UserRepository(User).get_by_api_key(db, credentials.credentials)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return report_repo.get_by_user_id(db, user.id)

@router.get("/device/{device_id}", response_model=List[ReportInDB])
def get_device_reports(
    device_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Получение списка отчетов для конкретного устройства.
    
    Доступно только для просмотра отчетов своих устройств.
    
    Args:
        device_id: ID устройства
        credentials: Данные авторизации
        db: Сессия базы данных
        
    Returns:
        List[ReportInDB]: Список отчетов устройства
        
    Raises:
        HTTPException: Если устройство не найдено или нет прав доступа
    """
    api_key = credentials.credentials
    device = db.query(Device).filter(Device.api_key == api_key).first()
    if not device:
        raise HTTPException(status_code=404, detail="Устройство не найдено")
    
    target_device = db.query(Device).filter(
        Device.id == device_id,
        Device.user_id == device.user_id
    ).first()
    
    if not target_device:
        raise HTTPException(status_code=404, detail="Устройство не найдено или доступ запрещен")
    
    return report_repo.get_by_device_id(db, device_id)

@router.get("/{report_id}", response_model=ReportInDB)
def get_report(
    report_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Получение информации об отчете по ID.
    
    Доступно только для просмотра своих отчетов.
    
    Args:
        report_id: ID отчета
        credentials: Данные авторизации
        db: Сессия базы данных
        
    Returns:
        ReportInDB: Информация об отчете
        
    Raises:
        HTTPException: Если отчет не найден или нет прав доступа
    """
    user = UserRepository(User).get_by_api_key(db, credentials.credentials)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    db_report = report_repo.get(db, id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Отчет не найден")
    
    if db_report.user_id != user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    return db_report
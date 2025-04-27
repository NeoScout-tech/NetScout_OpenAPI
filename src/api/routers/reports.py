from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

from src.database.config import get_db
from src.repositories.report import ReportRepository
from src.schemas.report import ReportCreate, ReportInDB
from src.models.device import Device
from src.models.report import Report
from src.models.user import User
from src.repositories.user import UserRepository

security = HTTPBearer()

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    dependencies=[Depends(security)]
)
report_repo = ReportRepository(Report)

@router.post("/", response_model=ReportInDB)
def create_report(
    report: ReportCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Create a new report.
    Available only for creating reports for own devices.
    
    Args:
        report: Report creation data
        credentials: Authorization data
        db: Database session
        
    Returns:
        ReportInDB: Created report
        
    Raises:
        HTTPException: If device not found or no access rights
    """
    api_key = credentials.credentials
    device = db.query(Device).filter(Device.api_key == api_key).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    report_data = report.model_dump()
    report_data["user_id"] = device.user_id
    return report_repo.create(db, obj_in=report_data)

@router.get("/", response_model=List[ReportInDB])
def get_reports(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get list of reports for current user.
    
    Args:
        credentials: Authorization data
        db: Database session
        
    Returns:
        List[ReportInDB]: List of user reports
    """
    user = UserRepository(User).get_by_api_key(db, credentials.credentials)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return report_repo.get_by_user_id(db, user.id)

@router.get("/device/{device_id}", response_model=List[ReportInDB])
def get_device_reports(
    device_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get list of reports for specific device.
    Available only for own devices.
    
    Args:
        device_id: Device ID
        credentials: Authorization data
        db: Database session
        
    Returns:
        List[ReportInDB]: List of device reports
        
    Raises:
        HTTPException: If device not found or no access rights
    """
    api_key = credentials.credentials
    device = db.query(Device).filter(Device.api_key == api_key).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    target_device = db.query(Device).filter(
        Device.id == device_id,
        Device.user_id == device.user_id
    ).first()
    
    if not target_device:
        raise HTTPException(status_code=404, detail="Device not found or access denied")
    
    return report_repo.get_by_device_id(db, device_id)

@router.get("/{report_id}", response_model=ReportInDB)
def get_report(
    report_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get report information by ID.
    Available only for viewing own reports.
    
    Args:
        report_id: Report ID
        credentials: Authorization data
        db: Database session
        
    Returns:
        ReportInDB: Report information
        
    Raises:
        HTTPException: If report not found or no access rights
    """
    user = UserRepository(User).get_by_api_key(db, credentials.credentials)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_report = report_repo.get(db, id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if db_report.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return db_report
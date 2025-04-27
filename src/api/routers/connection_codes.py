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
    Create a new connection code.
    Available only for creating codes in own account.
    
    Args:
        connection_code: Code creation data
        credentials: Authorization data
        db: Database session
        
    Returns:
        ConnectionCodeInDB: Created connection code
        
    Raises:
        HTTPException: If no rights to create code
    """
    user = UserRepository(User).get_by_api_key(db, credentials.credentials)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return connection_code_repo.create(db, obj_in=connection_code.model_dump())
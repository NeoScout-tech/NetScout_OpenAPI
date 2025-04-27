from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database.config import get_db
from src.repositories.user import UserRepository
from src.models.user import User

async def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    Get current user by API key from request header.
    
    Args:
        request: FastAPI request
        db: Database session
        
    Returns:
        User: User object
        
    Raises:
        HTTPException: If API key not provided or invalid
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
    Check if user is resource owner.
    
    Args:
        user_id: Resource owner user ID
        current_user: Current user
        
    Raises:
        HTTPException: If current user is not the owner
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions") 
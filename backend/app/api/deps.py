from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from app.database import get_db
from app.models.auth import User
from app.utils.security import SECRET_KEY, ALGORITHM, oauth2_scheme
from app.models.lookup import UserRole

def _verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    user_id = int(_verify_token(token).get("sub"))
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Wraps get_current_user and adds a role check.

    Raises 403 for any authenticated user whose role is not 'admin'.
    This dependency is applied to every route in this router.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )
    return current_user
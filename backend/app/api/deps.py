from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from app.database import get_db
from app.models.user import User
from app.utils.security import SECRET_KEY, ALGORITHM, oauth2_scheme

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
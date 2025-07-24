from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .auth import decode_access_token
from .database import SessionLocal
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        user = db.query(User).filter(User.username == payload.get("sub")).first()
        if user is None:
            raise HTTPException(status_code=401)
        return user
    except:
        raise HTTPException(status_code=401)

def require_role(required_role: str):
    def role_dependency(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(status_code=403, detail="Insufficient privileges")
        return user
    return role_dependency

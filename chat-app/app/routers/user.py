from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, auth, deps

router = APIRouter(tags=["Auth"])

@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_pw = auth.hash_password(user.password)
    new_user = models.User(username=user.username, password=hashed_pw, role=user.role)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(deps.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth.create_access_token(data={"sub": db_user.username, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}

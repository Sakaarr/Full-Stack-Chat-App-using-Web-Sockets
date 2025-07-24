from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, deps

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("/")
def create_room(room: schemas.RoomCreate, db: Session = Depends(deps.get_db)):
    existing = db.query(models.Room).filter(models.Room.name == room.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Room already exists")
    new_room = models.Room(name=room.name)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Message, Room, User
from datetime import datetime
from app.deps import require_admin
from sqlalchemy import func
import csv
from io import StringIO
from fastapi.responses import StreamingResponse
from sqlalchemy import cast, Integer


router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/messages-per-room",dependencies=[Depends(require_admin)])
def messages_per_room(db: Session = Depends(get_db)):
    results = db.query(
        Message.room_id,
        Room.name,
        func.count(Message.id).label("message_count")
    ).join(Room, cast(Room.id, Integer) == cast(Message.room_id, Integer))\
     .group_by(Message.room_id, Room.name)\
     .all()
    return [{"room_id": r.room_id, "room_name": r.name, "message_count": r.message_count} for r in results]


@router.get("/user-activity",dependencies=[Depends(require_admin)])
def user_activity(
    db: Session = Depends(get_db),
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
):
    query = db.query(User.username, func.count(Message.id).label("messages_sent"))\
              .join(Message, Message.sender_id == User.id)

    if start_date:
        query = query.filter(Message.timestamp >= start_date)
    if end_date:
        query = query.filter(Message.timestamp <= end_date)

    query = query.group_by(User.username)
    results = query.all()
    return [{"username": r.username, "messages_sent": r.messages_sent} for r in results]


@router.get("/export-messages-csv", dependencies=[Depends(require_admin)])
def export_messages_csv(db: Session = Depends(get_db)):
    results = db.query(Room.name, func.count(Message.id)).join(Room).group_by(Room.name).all()

    stream = StringIO()
    writer = csv.writer(stream)
    writer.writerow(["Room", "Message Count"])
    for name, count in results:
        writer.writerow([name, count])

    stream.seek(0)
    return StreamingResponse(stream, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=messages_report.csv"})
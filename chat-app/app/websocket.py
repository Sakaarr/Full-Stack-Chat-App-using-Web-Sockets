from fastapi import WebSocket, WebSocketDisconnect
from jose import JWTError
from typing import Dict, List
from .auth import decode_access_token
from .models import Message, Room, User
from .database import SessionLocal
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(room_id, []).append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        connections = self.active_connections.get(room_id, [])
        if websocket in connections:
            connections.remove(websocket)

    async def broadcast(self, room_id: str, message: dict):
        connections = self.active_connections.get(room_id, [])
        to_remove = []
        for connection in connections:
            try:
                await connection.send_json(message)
            except RuntimeError:
                to_remove.append(connection)

        for conn in to_remove:
            connections.remove(conn)

manager = ConnectionManager()

async def get_user_from_token(token: str):
    try:
        payload = decode_access_token(token)
        print(payload)
        return payload.get("sub")  # assumed to be username
    except JWTError:
        return None

async def chat_endpoint(websocket: WebSocket, room_id: str, token: str):
    username = await get_user_from_token(token)
    if not username:
        await websocket.close(code=1008)
        return

    await manager.connect(room_id, websocket)

    db = SessionLocal()
    try:
        user = db.query(User).filter_by(username=username).first()
        if not user:
            await websocket.close(code=1008)
            return

        # Send recent messages
        recent_messages = (
            db.query(Message)
            .filter(Message.room_id == room_id)
            .order_by(Message.timestamp.desc())
            .limit(20)
            .all()
        )
        for msg in reversed(recent_messages):
            sender = db.query(User).filter_by(id=msg.sender_id).first()
            await websocket.send_json({
                "username": sender.username if sender else "Unknown",
                "content": msg.content,
                "timestamp": str(msg.timestamp)
            })

        while True:
            data = await websocket.receive_json()
            content = data.get("content", "").strip()

            if not content:
                await websocket.send_json({"error": "Message cannot be empty."})
                continue

            message = Message(room_id=room_id, sender_id=user.id, content=content)
            db.add(message)
            db.commit()

            await manager.broadcast(room_id, {
                "username": username,
                "content": content,
                "timestamp": str(message.timestamp)
            })

            room = db.query(Room).filter(Room.name == room_id).first()
            if not room:
                await websocket.close(code=1003)
                return

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
    finally:
        db.close()

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class MessageSchema(BaseModel):
    room_id: str
    content: str
    
class RoomCreate(BaseModel):
    name: str
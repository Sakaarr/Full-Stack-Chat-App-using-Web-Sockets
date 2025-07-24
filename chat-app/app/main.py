from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user, chat, room

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(chat.router)
app.include_router(room.router)

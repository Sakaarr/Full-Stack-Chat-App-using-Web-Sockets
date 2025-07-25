# app/main.py

from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user, chat, room, analytics
from app.admin import setup_admin

app = FastAPI()
# Mount DB tables
Base.metadata.create_all(bind=engine)
# Initialize SQLAdmin
admin = setup_admin(app, engine)



# Include routers
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(room.router)
app.include_router(analytics.router)

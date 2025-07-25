# app/admin.py

from sqladmin import Admin, ModelView
from app.models import User, Room, Message

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.role]

class RoomAdmin(ModelView, model=Room):
    column_list = [Room.id, Room.name]

class MessageAdmin(ModelView, model=Message):
    column_list = [Message.id, Message.room_id, Message.sender_id, Message.content, Message.timestamp]

def setup_admin(app, engine):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(RoomAdmin)
    admin.add_view(MessageAdmin)
    return admin

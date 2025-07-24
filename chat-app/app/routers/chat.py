from fastapi import APIRouter, WebSocket, Query
from ..websocket import chat_endpoint

router = APIRouter()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, token: str = Query(...)):
    # token = websocket.query_params.get("token")
    try:
        # Token is already extracted by FastAPI from query parameters
        if not token:
            await websocket.close(code=1008)  # Policy Violation
            return
            
        await chat_endpoint(websocket, room_id, token)
    except Exception as e:
        # Log the error if needed
        print(f"WebSocket error: {e}")
        await websocket.close(code=1011) 

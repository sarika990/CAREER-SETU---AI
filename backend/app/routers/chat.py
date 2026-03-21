from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List
from ..auth import decode_access_token
from ..database import get_db
from datetime import datetime

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_email: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_email] = websocket

    def disconnect(self, user_email: str):
        if user_email in self.active_connections:
            del self.active_connections[user_email]

    async def send_personal_message(self, message: dict, receiver_email: str):
        if receiver_email in self.active_connections:
            await self.active_connections[receiver_email].send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    payload = decode_access_token(token)
    if not payload:
        await websocket.close(code=1008)
        return
    
    user_email = payload.get("sub")
    await manager.connect(user_email, websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            # data format: {"receiver": "email", "message": "text"}
            receiver_email = data.get("receiver")
            message_text = data.get("message")
            
            if receiver_email and message_text:
                msg_payload = {
                    "sender": user_email,
                    "message": message_text,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                # 1. Save to DB
                db = get_db()
                await db["chats"].insert_one({
                    "sender_id": user_email,
                    "receiver_id": receiver_email,
                    "message": message_text,
                    "timestamp": datetime.utcnow(),
                    "is_read": False
                })
                
                # 2. Forward to receiver if online
                await manager.send_personal_message(msg_payload, receiver_email)
                
    except WebSocketDisconnect:
        manager.disconnect(user_email)

@router.get("/history/{receiver_email}")
async def get_chat_history(receiver_email: str, token: str):
    payload = decode_access_token(token)
    if not payload:
        return {"error": "Unauthorized"}
    
    user_email = payload.get("sub")
    db = get_db()
    
    # Fetch messages between sub and receiver_email
    messages = await db["chats"].find({
        "$or": [
            {"sender_id": user_email, "receiver_id": receiver_email},
            {"sender_id": receiver_email, "receiver_id": user_email}
        ]
    }).sort("timestamp", 1).to_list(length=100)
    
    for m in messages:
        m["_id"] = str(m["_id"])
        
    return messages

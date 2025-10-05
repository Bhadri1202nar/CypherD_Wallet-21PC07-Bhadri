from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import wallet, transactions, notifications
from app.auth import router as auth_router
import json

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mock Web3 Wallet API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, wallet_address: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[wallet_address] = websocket

    def disconnect(self, wallet_address: str):
        if wallet_address in self.active_connections:
            del self.active_connections[wallet_address]

    async def send_personal_message(self, message: str, wallet_address: str):
        if wallet_address in self.active_connections:
            await self.active_connections[wallet_address].send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{wallet_address}")
async def websocket_endpoint(websocket: WebSocket, wallet_address: str):
    await manager.connect(wallet_address, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for heartbeat
            await websocket.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        manager.disconnect(wallet_address)

@app.get("/")
async def root():
    return {
        "message": "Mock Web3 Wallet API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
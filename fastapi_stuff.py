from fastapi import Depends , WebSocket , WebSocketDissconect
from sqlalchemy.ext.asyncio import AsyncSession , create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("postgresql+asyncpg:://matan:matan123@localhost:5432/backend_stuff")
async_session = sessionmaker(engine , class_=AsyncSession , expire_on_commit=False)

#here we create the dependency for the websocket request to yeild a new db
# connection everytime
async def generate_db() -> AsyncGenerator[AsyncSession , None]:
    async with async_session() as session:
        yield session

# this is the code for the actual connection to the "chat room".
#in this class we just keep track on who is connected , theres a method for
#connect , disconnect , and to broadcast msgs to everyone
class ConnectionManager:
    def __init__(self):
        self.active_connections : list[WebSocket] = []

    async def connect(self , websocket : WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self , websocket : WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def broadcast(self , message : str) -> None:
        for connection in self.active_connections:
            await connection.send_text(message)

#giving a var to the class
manager = ConnectionManager

@app.websocket("/ws")
async def websocket_server(websocket : WebSocket , db : AsyncSession = Depends(generate_db)) -> None:
    manager.connect(websocket)
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_text() 
            with AsyncSession as session:
                statement = insert(messages).values(username=(idfkyetbro),Messages=msg)
                result = await session.execute(statement)
            websocket.broadcast(msg)
        except WebSocketDisconnect:
            print('someone dced')



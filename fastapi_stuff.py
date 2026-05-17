from fastapi import FastAPI , Depends , WebSocket , WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession , create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from msgs_sqlalchemy import Auth , User , Messages
from pydantic import ValidationError
from typing import Dict
engine = create_async_engine(async_engine)
async_session = sessionmaker(engine , class_=AsyncSession , expire_on_commit=False)

# this is the code for the actual connection to the "chat room".
#in this class we just keep track on who is connected , theres a method for
#connect , disconnect , and to broadcast msgs to everyone
class ConnectionManager:
    def __init__(self):
        self.active_connections : Dict[str , WebSocket] = {}
    
    async def first_entry(self , websocket : WebSocket) -> None:
        await websocket.accept()

    async def connect(self , username : str , websocket : WebSocket) -> None:
        self.active_connections[username] = websocket
    
    def disconnect(self , username : str) -> None:
        if username in self.active_connections:
            del self.active_connections[username]

    async def broadcast(self , message : str) -> None:
        for connection in self.active_connections.values():
            try:
                await connection.send_text(message)
            except Exception:
                pass
#giving a var to the class
app = FastAPI()
manager = ConnectionManager()

async def auth_stuff(auth : Auth , session : AsyncSession) -> tuple[str,User]:
    username_notdb = auth.username
    password_notdb = auth.password
    statement = select(User).where(User.username == username_notdb)
    result = await session.execute(statement)
    user = result.scalars().first()

    if user is None:
        new_user = User(username=username_notdb , password=password_notdb)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return f'account created : {username_notdb}:{password_notdb}' , new_user
    if user.password == password_notdb:
        return f'connected' , user
    else:
        raise ValueError('wrong password')
    
@app.websocket("/ws")
async def websocket_server(websocket : WebSocket) -> None:
    await manager.first_entry(websocket)
    username = None
    current_user = None
    try:
        while True:
            await websocket.send_text("enter your username/password in this format: 'username:password")
            auth_msg = await websocket.receive_text()
            try:
                auth_data = Auth.get_string(auth_msg)

                async with async_session() as session:
                   status_text , current_user = await auth_stuff(auth_data , session)

                username = auth_data.username
                if username in manager.active_connections:
                    await websocket.send_text("user logged in from somewhere else")
                    await websocket.close()
                    return
                await manager.connect(username , websocket)
                await websocket.send_text(status_text)
                break
            except ValueError as error:
                await websocket.send_text(f'somethings wrong {error}')
            except ValidationError:
                await websocket.send_text(f'the msg you sent was too long only 50 chars')      
        while True:
            msg_notdb = await websocket.receive_text()
            if len(msg_notdb) > 50:
                await websocket.send_text("msg too long (max 50)")
                continue
            async with async_session() as session:
                new_msg = Messages(user_id=current_user.id , msg=msg_notdb)
                session.add(new_msg)
                await session.commit()
            await manager.broadcast(f'{username}: {msg_notdb}')
    except WebSocketDisconnect:
        if username:
            manager.disconnect(username)
            await manager.broadcast(f'{username} left')

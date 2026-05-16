from fastapi import Depends , WebSocket , WebSocketDissconect
from sqlalchemy.ext.asyncio import AsyncSession , create_async_engine
from sqlalchemy.orm import sessionmaker
from msgs_sqlalchemy import Auth
from pydantic import ValidationError
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
        self.active_connections : Dict[str , WebSocket] = {}
    
    async def first_entry(self , websocket : WebSocket) -> None:
        await websocket.accept()

    async def connect(self , username = str , websocket : WebSocket) -> None:
        self.active_connections[username] = websocket
    
    def disconnect(self , username : str , websocket : WebSocket) -> None:
        if username in self.active_connections:
            del self.active_connections[username]

    async def broadcast(self , message : str) -> None:
        for connection in self.active_connections.values():
            await connection.send_text(message)

#giving a var to the class
manager = ConnectionManager

async def auth_stuff(auth : Auth , session : async_session)->:
    username_notdb = auth.username
    password_notdb = auth.password
    check_username = await session.execute(User).where(User.username == username_notdb)
    user = result.scalar().first()
    if user is None:
        new_user = User(username=username_notdb , password=password_notdb)
        await session.add(new_user)
        return (f'account created : {username_notdb}:{password_notdb}')
    if user.password == password_notdb:
        return (f'connected')
    else:
        raise ValueError('wrong password')
    
@app.websocket("/ws")
async def websocket_server(websocket : WebSocket , db : AsyncSession = Depends(generate_db)) -> None:
    manager.first_entry(websocket)
    await websocket.accept()
    try:
        while True:
            await websocket.send_text("enter your username/password in this format: 'username:password")
            auth_msg = await websocket.receive_text()
            auth_data = Auth.get_string(auth_msg)

            async with AsyncSession as session:
                checking = await auth_stuff(auth_data , session)

            username = auth_data.username
            manager.connect(username , websocket)
            break
    except ValueError as error:
        await websocket.send_text(f'somethings wrong {error}')
    except ValidationError:
        await websocket.send_text(f'the msg you sent was too long only 50 chars')
        while True:
            msg = await websocket.receive_text()
            async with AsyncSession as session
                statement = insert(Messages).values(user_id = (User.id).where(User.username == auth_data.username),Messages=msg)
                result = await session.execute(statement)
            websocket.broadcast(msg)
        except WebSocketDisconnect:
            print('someone dced')

            await manager.broadcast(f'{username}: {msg}')


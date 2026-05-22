## real-time Async chatroom

real-time chatroom backend built to handle concurrent user connections, user auth , and message history. 

## Tech Stack
- Database: PostgreSQL
- ORM: SQLAlchemy 2.0 (Async/sync)
-  Framework: FastAPI (WebSockets)
-  Data Validation: Pydantic v2

## What I learned building this

the project isnt necessarily hard or complicated its just the first "big" thing Ive built. the reason I built it was purely for learning , I got interested in async programming and databases and tried to think of a project that could help me learn that , further more this project was kinda my introduction to APIs.

big "milestones" of the project:
- managing connection states: made a `ConnectionManager` class to store active WebSocket connections in a dictionary, handle new logins, broadcast messages to everyone, and clean up when someone leaves.
- using sync and async SQLAlchemy: used standard `create_engine` to handle server side table creation, but switched to `create_async_engine` and `AsyncSession` for the actual chat server so database calls doesnt block the WebSocket connections.
- handling blocking I/O in asyncio: nn the client side, standard python `input()` blocks the whole code. I learned how to use `loop.run_in_executor` to change the user input to a separate thread so the client can still receive incoming messages while typing.
- data validation: made text limits (like a max 50 char message limit) on both the pydantic model and the database schema layer.
### IMPORTANT : no ai was used in this project , everything I did here I either learned from reading docs/viewing other people's projects/figuring stuff out by myself . you can find all the notes Ive made on sqlalchemy/fastapi in my notes repo
# How it works
### 1. Connection 
The user runs `connection.py` and enters the host server's ip. the client attempts to open a WebSocket connection at the `/ws` endpoint, and the server accepts it onto the next phase.

### 2. The Auth Process
before joining the chat, the server demands a login string as followed: `username:password`.
- parsing: The server passes the string to a Pydantic func (`Auth.get_string`) which splits the input.
- DB check: the server queries PostgreSQL using an async session which gets all the usernames/passwords from the db:
  - new_user: If the username isnt found in the query, the server automatically registers them, inserts the credentials, and returns a `account created` string.
  - existing_user: if the username exists, it checks the password. if its wrong,it throws an error and disconnects them.
-check for multiple connections: if the username is already active in the server's connection dict, the server straight up closes the sockets so there wont be double logins.

### 3. The chat loop
if the auth proccess finishes smoothly, the user is added to the active connections list. the client uses `asyncio.gather` to run two loops at the same time:
- incoming: listens for broadcasts from the server and prints them to the terminal.
- outgoing: waits for user to type a new msg. when a msg is typed, the server checks its under 50 chars,inserts it to the PostgreSQL `Messages` table with a UTC timezone, and broadcasts it as (`username: message`) to everyone in the room.

### 4. Disconnect
If a user closes their terminal or loses connection, the server catches the `WebSocketDisconnect` exception, deletes their socket from the active dict, and broadcasts a message to the room letting everyone know that user left.

## Requirements

- The client requires a third party library called : `websockets` library installed.
- gotta be in the same network

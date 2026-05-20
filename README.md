# Real time chatroom backend

project combines multiple python libraries to create a real time chatroom with authorazation and database which tracks the msgs.
# tech stack used:
- Database : PostgreSql
- ORM : SqlAlchemy
- for the API : FastAPI[websockets]

# and other libraries which do play a role in this project but are not the "MAIN" course:
- asyncio
- websockets
- typing
- pydantic
- datetime

# REQS
the way this works is quite simple , but there are a few requierments on the client's side:
-they should have the websockets library installed as its not in the psl.
-the client has to be in the same network as me for this to work.

# some explaining about the project
im gonna yap abit about the flow of the project , wont go into to much depth:
the client runs the connections.py file which asks him for an ip , I provide him my ip and he types it out , now the auth proccess begins.
he connects to the server through websockets and receives a text which guides him on how to send his username and password.
the client sends his info(if you wanna know how the proccess of auth happens just go look at the project if you wanna know the details) a db connection open and checks if hes even in the db , if hes not it just adds him with his password , if he is , it checks if the password is correct. if its not well he just disconnects
.
after hes connected an "async loop" starts running that allows him to send/recieve msgs , and everytime someone sends a msg its sent into the db aswell.

# yap sesh
the project isnt neceserly hard or complicated its just the first "big" thing Ive built
the reason I built it was purely for learning , I got intrested in async programming and databases and tried to think of a project that could help me learn that , further more this project was kinda my introduction to APIs.

NO AI WAS USED FOR WRITING THE CODE , I had to learn this by myself through reading docs/viewing others people projects/and just trying to understand it myself , Ive provided notes for everything in my notes repo if someone is in need of them.


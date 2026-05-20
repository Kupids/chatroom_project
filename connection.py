import asyncio
import websockets

async def get_msg(websocket) -> None:
    try:
        async for message in websocket:
            print(message)
            print("send msg: " , flush=True)
    except websockets.exceptions.ConnectionClosed:
        print("dced")

async def send_msg(websocket):
    print("connected!")
    while True:
        loop = asyncio.get_event_loop()
        msg = await loop.run_in_executor(None , input , "send msg: ")

        if msg.strip():
            try:
                await websocket.send(msg)
            except websockets.exceptions.ConnectionClosed:
                break
async def main():
    ip = str(input("enter the ip address please dont fuck up"))
    try:
        async with websockets.connect(f'ws://{ip}:8000/ws') as websocket:
            server_msg = await websocket.recv()
            print(f'SERVER: {server_msg}')
            auth_msg = str(input("send your username/password in this format= username:password (for example matan:2025pass):"))
            await websocket.send(auth_msg)
            server_respons = await websocket.recv()
            print(f'SERVER: {server_respons}')

            if "connected" in server_respons or "account created" in server_respons:
                await asyncio.gather(
                    get_msg(websocket),
                    send_msg(websocket)
                    )
            else:
                print("something went wrong")
    except Exception as error:
        print(f'something went wrong: {error}')

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bye")

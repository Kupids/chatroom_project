from fastapi import FastAPI

app = FastAPI()

@app.get("/home/matan/testing_apy.py")
async def test(item : str) -> str:
    return {"item" : item} 



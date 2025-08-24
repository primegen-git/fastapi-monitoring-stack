from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def greet():
    return {"welcome to vibe monitor"}

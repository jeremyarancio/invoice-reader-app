from fastapi import FastAPI

from settings import SRC_DIR


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
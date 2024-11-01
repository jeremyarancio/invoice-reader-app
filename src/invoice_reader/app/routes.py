from fastapi import FastAPI

from invoice_reader.settings import SRC_DIR


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
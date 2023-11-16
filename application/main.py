import uvicorn
import os

from fastapi import FastAPI, HTTPException


app = FastAPI(
    title="Parsing app"
)

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True, workers=3)


@app.get("/")
def hello_world():
    return "Hello, world!"
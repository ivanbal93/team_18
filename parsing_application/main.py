import uvicorn

from fastapi import FastAPI, HTTPException

from database import database


app = FastAPI(
    title="Parsing app"
)

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True, workers=3)


@app.on_event("startup")
async def startup_database():
    '''Подключение к БД'''
    await database.connect()


@app.on_event("shutdown")
async def shutdown_database():
    '''Отключение от БД'''
    await database.disconnect()


@app.get("/")
def hello_world():
    return "Hello, world!"

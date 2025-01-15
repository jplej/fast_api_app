from fastapi import FastAPI
from app.db import init_db, close_db
from app.models import User

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.post("/users/")
async def create_user(name: str, email: str):
    user = await User.create(name=name, email=email)
    return user

from fastapi import FastAPI
from src.db import init_db, close_db
from src.models import User
from src.redis import redis_client

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

@app.get('/redis')
async def read_redis():
    redis_client.set('message', 'hellow redis')
    message = redis_client.get('message')
    return {'message': message}
    

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.db import init_db, close_db
from src.redis import redis_client
from src.celery import celery_client
from src.routers import auth, users, questrade, health


app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(questrade.router)
app.include_router(health.router)


@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()
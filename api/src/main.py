from fastapi import FastAPI
from src.db import init_db, close_db
from src.routers import auth, users, health, stock 


app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(health.router)
app.include_router(stock.router)


@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()
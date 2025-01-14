from fastapi import FastAPI

# Create a FastAPI instance
app = FastAPI()

# Define a root route
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

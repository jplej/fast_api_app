from fastapi import APIRouter, HTTPException, Depends
from tortoise.transactions import in_transaction
from pydantic import BaseModel
from src.models import Users, QuestradeApiKeys 

router = APIRouter(
    prefix='/questrade',
    tags=['questrade']
)

class AddApiKeyRequest(BaseModel):
    user_id: int
    api_key: str


@router.post("/api-keys", response_model=dict)
async def create_api_key(request: AddApiKeyRequest):
    async with in_transaction():
        user = await Users.get_or_none(user_id=request.user_id) 
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        existing_api_key = await QuestradeApiKeys.get_or_none(user_id=user) 
        if existing_api_key:
            raise HTTPException(status_code=400, detail="API key already exists for this user")
        
        await QuestradeApiKeys.create(user_id=user, api_key=request.api_key)
        return {"message": "API key created successfully"}


@router.put("/api-keys", response_model=dict)
async def update_api_key(request: AddApiKeyRequest):
    async with in_transaction():
        api_key_entry = await QuestradeApiKeys.get_or_none(user_id=request.user_id) 
        if not api_key_entry:
            raise HTTPException(status_code=404, detail="API key does not exist for this user")
        
        api_key_entry.api_key = request.api_key
        await api_key_entry.save()
        return {"message": "API key updated successfully"}


@router.delete("/api-keys/{user_id}", response_model=dict)
async def delete_api_key(user_id: int):
    async with in_transaction():
        api_key_entry = await QuestradeApiKeys.get_or_none(user_id=user_id)  
        if not api_key_entry:
            raise HTTPException(status_code=404, detail="API key not found")
        
        await api_key_entry.delete()
        return {"message": "API key deleted successfully"}


# GET endpoint: Fetch the API key by user ID
@router.get("/api-keys/{user_id}", response_model=dict)
async def get_api_key(user_id: int):
    api_key_entry = await QuestradeApiKeys.get_or_none(user_id=user_id)  
    if not api_key_entry:
        raise HTTPException(status_code=404, detail="API key not found")
    
    return {"user_id": user_id, "api_key": api_key_entry.api_key}

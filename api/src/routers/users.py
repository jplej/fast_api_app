from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Path
from tortoise.exceptions import DoesNotExist
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext
from src.models import Users

router = APIRouter(
    prefix='/user',
    tags=['user']
)


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
user_dependency = Annotated[dict, Depends(get_current_user)]



class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str = Field(min_length=6)
    role: str
    phone_number: str = None

class UpdateUserRequest(BaseModel):
    email: str = None
    first_name: str = None
    last_name: str = None
    role: str = None
    phone_number: str = None
   
class UpdatePasswordRequest(BaseModel):
    new_password: str = Field(min_length=6)


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_request: CreateUserRequest):
    new_user = Users(
        email=user_request.email,
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        hashed_password=bcrypt_context.hash(user_request.password),
        role=user_request.role,
        phone_number=user_request.phone_number,
        is_active=True,
    )
    await new_user.save()
    return {"message": "User created successfully", "user_id": new_user.user_id}



@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = await Users.get(id=user.get('id'))
    if not user_model:
        raise HTTPException(status_code=404, detail='User not found')
    return user_model


@router.put("/", status_code=status.HTTP_200_OK)
async def update_user(user_request: UpdateUserRequest, user: user_dependency):
    try:
        user_model = await Users.get(user_id=user.get("id"))
        if user_request.email:
            user_model.email = user_request.email
        if user_request.first_name:
            user_model.first_name = user_request.first_name
        if user_request.last_name:
            user_model.last_name = user_request.last_name
        if user_request.role:  # Optional: Ensure only admins can change roles
            raise HTTPException(status_code=403, detail="Cannot change role")
        if user_request.phone_number:
            user_model.phone_number = user_request.phone_number
        await user_model.save()
        return {"message": "User updated successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/change_password", status_code=status.HTTP_200_OK)
async def change_password(password_request: UpdatePasswordRequest, user: user_dependency):
    try:
        user_model = await Users.get(user_id=user.get("id"))
        hashed_password = bcrypt_context.hash(password_request.new_password)
        user_model.hashed_password = hashed_password
        await user_model.save()
        return {"message": "Password updated successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: user_dependency):
    try:
        user_model = await Users.get(user_id=user.get("id"))
        await user_model.delete()
        return {"message": "User deleted successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")









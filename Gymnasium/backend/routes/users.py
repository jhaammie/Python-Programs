from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime
from hoohoohee import GetUserById, UpdateUser
from .auth import get_current_user, UserBase

router = APIRouter()

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

@router.get("/users/me", response_model=UserResponse)
async def get_current_user_info(current_user: UUID = Depends(get_current_user)):
    user = GetUserById(str(current_user))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": UUID(user[0]),
        "email": user[1],
        "first_name": user[3],
        "last_name": user[4],
        "created_at": user[5],
        "updated_at": user[6]
    }

@router.put("/users/me", response_model=UserResponse)
async def update_user_info(
    user_update: UserUpdate,
    current_user: UUID = Depends(get_current_user)
):
    user = GetUserById(str(current_user))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user
    updated_at = datetime.utcnow()
    success = UpdateUser(
        str(current_user),
        user_update.email or user[1],
        user_update.password,
        user_update.first_name or user[3],
        user_update.last_name or user[4],
        updated_at
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update user")
    
    # Get updated user
    updated_user = GetUserById(str(current_user))
    return {
        "id": UUID(updated_user[0]),
        "email": updated_user[1],
        "first_name": updated_user[3],
        "last_name": updated_user[4],
        "created_at": updated_user[5],
        "updated_at": updated_user[6]
    } 
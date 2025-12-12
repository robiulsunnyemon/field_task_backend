from fastapi import APIRouter, HTTPException, Depends,status
from typing import List

from field_task.auth.models.user_model import UserModel
from field_task.auth.schemas.user_schemas import UserResponse, UserUpdate


user_router = APIRouter(prefix="/users", tags=["Users"])

# GET all users
@user_router.get("/", response_model=List[UserResponse],status_code=status.HTTP_200_OK)
async def get_all_users(skip: int = 0, limit: int = 200):
    """
    Get all users with pagination
    """
    users = await UserModel.find_all().skip(skip).limit(limit).to_list()
    return users


# GET user by ID
@user_router.get("/{id}", response_model=UserResponse,status_code=status.HTTP_200_OK)
async def get_user(id: str):
    """
    Get user by ID
    """
    user = await UserModel.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# PATCH update user
@user_router.patch("/{id}", response_model=UserResponse,status_code=status.HTTP_200_OK)
async def update_user(id: str, user_data: UserUpdate):
    """
    Update user information
    """
    user = await UserModel.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_data.model_dump(exclude_unset=True)
    await user.update({"$set": update_data})
    return await UserModel.get(id)


# DELETE user
@user_router.delete("/{id}",status_code=status.HTTP_200_OK)
async def delete_user(id: str):
    """
    Delete user by ID
    """
    user = await UserModel.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete()
    return {"message": "User deleted successfully"}


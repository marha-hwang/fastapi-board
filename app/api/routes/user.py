from typing import Any
from fastapi import APIRouter
from app.schema.common import ApiRequest, ApiResponse
from app.schema.user import UserCreate, UserDelete, UserUpdate, UserPasswordChange
import app.crud.user as cruduser
import app.model.user as model_user
from fastapi import Depends
from app.core.security import get_current_user


router = APIRouter(tags=["사용자"], prefix="/user")

@router.post("", response_model=ApiResponse)
async def create_user(user_in: UserCreate) -> Any:

    result = await cruduser.insert_user(user=user_in)
    response = ApiResponse(success=True, message=result) 

    return response

@router.delete("", response_model=ApiResponse)
async def remove_user(current_user: str = Depends(get_current_user)) -> Any:

    result = await cruduser.delete_user(user=current_user)
    response = ApiResponse(success=True, message=result) 

    return response

@router.put("", response_model=ApiResponse)
async def update_user(user_in: UserUpdate) -> Any:


    result = await cruduser.update_user(user=user_in)
    response = ApiResponse(success=True, message=result) 

    return response

@router.put("/password", response_model=ApiResponse)
async def update_password(user_in: UserPasswordChange) -> Any:

    result = await cruduser.update_password(user=user_in)
    response = ApiResponse(success=True, message=result) 

    return response
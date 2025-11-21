from typing import Any
from fastapi import APIRouter
from app.core.security import get_current_user
import app.schema.common_schema as common_schema
import app.schema.user_schema as user_schema
import app.service.user_service as user_service

from fastapi import Depends
from app.core.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(tags=["사용자"], prefix="/user")

@router.post("", response_model=common_schema.ApiResponse)
async def create_user(request: user_schema.UserCreate, db: Session = Depends(get_db)) -> Any:

    result = user_service.create_user(input=request, db=db)
    response = common_schema.ApiResponse(success=True, message=result) 

    return response

@router.delete("", response_model=common_schema.ApiResponse)
async def remove_user(current_user: str = Depends(get_current_user)) -> Any:

    result = user_service.remove_user(user_id=current_user)
    response = common_schema.ApiResponse(success=True, message=result) 

    return response

@router.put("", response_model=common_schema.ApiResponse)
async def update_user(request: user_schema.UserUpdate, current_user: str = Depends(get_current_user)) -> Any:

    result = user_service.update_user(input=request, user_id=current_user)
    response = common_schema.ApiResponse(success=True, message=result) 

    return response

@router.put("/password", response_model=common_schema.ApiResponse)
async def update_password(request: user_schema.UserPasswordChange, current_user: str = Depends(get_current_user)) -> Any:

    result = user_service.update_password(input=request, user_id=current_user)
    response = common_schema.ApiResponse(success=True, message=result) 

    return response
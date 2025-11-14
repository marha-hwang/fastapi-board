from typing import Any
from fastapi import APIRouter
from fastapi import Depends
from app.core.security import get_current_user
import app.schema.common_schema as common_schema
import app.schema.comment_schema as comment_schema
import app.service.comment_service as comment_service


router = APIRouter(tags=["댓글"], prefix="/comment")

@router.post("", response_model=common_schema.ApiResponse)
async def create_comment(request: comment_schema.CommentCreateReq, current_user: str = Depends(get_current_user)) -> Any:

    result = comment_service.create_comment(input=request, user_id=current_user)
    response = common_schema.ApiResponse(success=True, message=result) 

    return response

@router.delete("", response_model=common_schema.ApiResponse)
async def remove_comment(request: comment_schema.CommentDeleteReq, current_user: str = Depends(get_current_user)) -> Any:

    result = comment_service.remove_comment(input=request, user_id=current_user)
    response = common_schema.ApiResponse(success=True, message=result) 

    return response

@router.put("", response_model=common_schema.ApiResponse)
async def update_comment(request: comment_schema.CommentUpdateReq, current_user: str = Depends(get_current_user)) -> Any:

    result = comment_service.update_comment(input=request, user_id=current_user)
    response = common_schema.ApiResponse(success=True, message=result) 

    return response

@router.get("/{post_id}", response_model=common_schema.ApiResponse)
async def view_list_comment(post_id:str, current_user: str = Depends(get_current_user)) -> Any:

    result = comment_service.get_comment_list(post_id=post_id)

    if result == None : return common_schema.ApiResponse(success=True, message="댓글이 존재하지 않습니다.") 

    response = common_schema.ApiResponse[comment_schema.CommentListRes](success=True, message="댓글 조회에 성공하였습니다.", data=result) 
    return response
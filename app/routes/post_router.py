from typing import Any
from fastapi import APIRouter
from fastapi import Depends
from app.core.security import get_current_user
import app.schema.common_schema as common_schema
import app.schema.post_schema as post_schema
import app.service.post_service as post_service


router = APIRouter(tags=["게시글"], prefix="/post")

@router.post("", response_model=common_schema.ApiResponse)
async def create_post(request: post_schema.PostCreateReq, current_user: str = Depends(get_current_user)) -> Any:

    result = post_service.create_post(input=request, user_id=current_user)
    response = common_schema.ApiResponse(success=True,
                                        message="게시글 작성에 성공하였습니다.",
                                        data=post_schema.PostCreateRes(post_id=result)) 

    return response

@router.delete("", response_model=common_schema.ApiResponse)
async def remove_post(request: post_schema.PostDeleteReq, current_user: str = Depends(get_current_user)) -> Any:

    result = post_service.remove_post(input=request, user_id=current_user)
    response = common_schema.ApiResponse(success=True, message=result) 

    return response

@router.put("", response_model=common_schema.ApiResponse)
async def update_post(request: post_schema.PostUpdateReq, current_user: str = Depends(get_current_user)) -> Any:

    result = post_service.update_post(input=request, user_id=current_user)
    response = common_schema.ApiResponse(success=True, message=result) 

    return response

@router.get("", response_model=common_schema.ApiResponse)
async def view_list_post(current_user: str = Depends(get_current_user)) -> Any:

    result = post_service.get_post_list()

    if result == None : return common_schema.ApiResponse(success=True, message="게시글이 존재하지 않습니다.") 

    response = common_schema.ApiResponse[post_schema.PostListRes](success=True, message="게시글 조회에 성공하였습니다.", data=result) 
    return response

@router.get("/{post_id}", response_model=common_schema.ApiResponse)
async def view_detail_post(post_id:str, current_user: str = Depends(get_current_user)) -> Any:

    result = post_service.get_post_detail(post_id=post_id, user_id=current_user)

    if result == None : return common_schema.ApiResponse(success=True, message="게시글이 존재하지 않습니다.") 

    response = common_schema.ApiResponse[post_schema.PostDetailRes](success=True, message="게시글 조회에 성공하였습니다.", data=result) 
    return response

@router.post("/like", response_model=common_schema.ApiResponse)
async def update_post_like(request: post_schema.PostLikeReq, current_user: str = Depends(get_current_user)) -> Any:

    result = post_service.update_post_like(input=request, user_id=current_user)
    response = common_schema.ApiResponse(success=True, message=result) 

    return response
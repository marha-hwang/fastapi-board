from typing import Any
import os
from fastapi import APIRouter, UploadFile
import app.schema.common_schema as common_schema
import app.config as config
import app.schema.file_schema as file_schema
from app.core.security import get_current_user
from fastapi import Depends
from app.core.database import get_db
from sqlalchemy.orm import Session
import app.service.file_service as file_service
from app.repository.base_file_repository import BaseFileRepository
from app.repository.db.db_file_repository import FileRepositoryDB
from app.repository.csv.csv_file_repository import FileRepositoryCSV

router = APIRouter(tags=["파일"], prefix="/file")

def get_file_repository(db:Session = Depends(get_db)):
    if config.db_type == "database" :
        return FileRepositoryDB(db)
    else:
        return FileRepositoryCSV()

@router.post("/upload", response_model=common_schema.ApiResponse)
async def upload_file(request: UploadFile, current_user: str = Depends(get_current_user), repo:BaseFileRepository = Depends(get_file_repository)) -> Any:

    result = await file_service.upload_file(repo, request)
    response = common_schema.ApiResponse(success=True,
                                        message="파일 업로드에 성공하였습니다.",
                                        data=file_schema.FileUploadRes(file_id=result)) 
    return response

@router.post("/download", response_model=common_schema.ApiResponse)
async def download_file(request: file_schema.FileDownloadReq, current_user: str = Depends(get_current_user), repo:BaseFileRepository = Depends(get_file_repository)) -> Any:

    result = file_service.download_file(repo, request.file_id)
    response = common_schema.ApiResponse(success=True,
                                        message="파일 조회에 성공하였습니다.",
                                        data=file_schema.FileDownloadRes(file_url=result)) 
    return response
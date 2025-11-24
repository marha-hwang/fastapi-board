import app.schema.file_schema as file_schema
import app.model.models as app_models
import app.core.security as security
from app.repository.base_file_repository import BaseFileRepository
import logging
from app.core.exception import CustomException, ErrorCode
import os
import shutil
import uuid
from fastapi import UploadFile

logger = logging.getLogger(__name__)

async def upload_file(repo:BaseFileRepository, data:UploadFile)->str:
    
    UPLOAD_DIR = "images"
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # 파일명 중복 방지를 위해 UUID 사용
    file_uuid = str(uuid.uuid4())


    # 원본 파일의 확장자 추출 (예: .jpg)
    file_extension = os.path.splitext(data.filename)[1]
    # 새로운 파일명 생성 (예: 550e8400-e29b... .jpg)
    new_filename = f"{file_uuid}{file_extension}"
    
    # 저장할 전체 경로
    file_path = os.path.join(UPLOAD_DIR, new_filename)

    # 서버 디스크에 파일 저장 (shutil 이용)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(data.file, buffer)

    try :
        repo.insert_file(app_models.File(img_id=file_uuid, img_url=file_path))
        return file_uuid
    
    except Exception as e:
        logger.error("error", exc_info=True)
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="파일 업로드에 실패하였습니다.")

def download_file(repo:BaseFileRepository, file_id:str)->str:
    try :
        return repo.select_file(img_id=file_id).img_url
    except Exception as e:
        logger.error("error", exc_info=True)
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="파일 조회에 실패하였습니다.")

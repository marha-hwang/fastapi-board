import app.schema.user_schema as user_schema
import app.model.models as app_models
import app.core.security as security
from app.repository.base_user_repository import BaseUserRepository
import logging
from app.core.exception import CustomException, ErrorCode

logger = logging.getLogger(__name__)

def create_user(repo:BaseUserRepository, data:user_schema.UserCreate) :
    if repo.select_user(user_id=data.user_id) != None : 
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="이미 등록된 사용자입니다.")

    hashedPassword = security.get_password_hash(data.password)
    user = app_models.User(
        user_id=data.user_id,
        password=hashedPassword,
        nickname=data.nickname,
        img_id=data.img_id
    )
    try :
        repo.insert_user(user)
    except Exception as e:
        logger.error("error", exc_info=True)
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="회원가입에 실패하였습니다.")

def remove_user(repo:BaseUserRepository, user_id:str) :
    if repo.select_user(user_id) == None :
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="등록되지 않은 사용자입니다.")

    try :
        repo.delete_user(user_id)
    except Exception as e:
        logger.error("error", exc_info=True)
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="회원삭제에 실패하였습니다.")

def update_user(repo:BaseUserRepository, data:user_schema.UserUpdate, user_id:str) :
    
    if repo.select_user(user_id) == None :
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="등록되지 않은 사용자입니다.")
    
    user = app_models.User(
        user_id=user_id,
        password="",
        nickname=data.nickname,
        img_id=data.img_id
    )

    try :
        repo.update_user(user)
    except Exception as e:
        logger.error("error", exc_info=True)
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="회원 업데이트에 실패하였습니다.")

def update_password(repo:BaseUserRepository, data:user_schema.UserPasswordChange, user_id:str) :

    if repo.select_user(user_id) == None : 
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="등록되지 않은 사용자입니다.")

    hashedPassword = security.get_password_hash(data.new_password)
   
    try :
        repo.update_password(hashedPassword, user_id)
    except Exception as e:
        logger.error("error", exc_info=True)
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="비밀번호 업데이트에 실패하였습니다.")


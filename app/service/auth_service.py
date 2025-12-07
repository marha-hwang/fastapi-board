import app.schema.auth_schema as auth_schema
import app.model.models as models
import app.core.security as security
from app.repository.base_user_repository import BaseUserRepository
import logging
from app.core.exception import CustomException, ErrorCode

logger = logging.getLogger(__name__)

def veryfy_user(repo:BaseUserRepository, data: auth_schema.Login)->tuple[auth_schema.UserInfo, str]:

    user = repo.select_user(data.user_id)
    if user == None :
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="로그인 정보가 올바르지 않습니다.")

    # 회원비밀번호 검증
    if not security.verify_password(data.password, user.password) : 
        raise CustomException(code=ErrorCode.NOT_AUTHENTICATED, message="로그인 정보가 올바르지 않습니다.")

    # jwt토큰 발급
    jwt = security.create_access_token(data={col.name: getattr(user, col.name) for col in user.__table__.columns})

    logger.info(f"{user.img_id} / {user.nickname}")
    userInfo = auth_schema.UserInfo(
        user_id=user.user_id,
        nickname=user.nickname,
        img_id=user.img_id if user.img_id != None else ""
    )

    return (userInfo, jwt)
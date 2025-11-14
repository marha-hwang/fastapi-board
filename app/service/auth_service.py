import app.schema.auth_schema as auth_schema
import app.model.models as models
import app.core.security as security
import app.crud.user_crud as user_crud
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def veryfy_user(input: auth_schema.Login)->tuple[auth_schema.UserInfo, str]:

    # 회원존재 검증
    user:models.User = user_crud.select_user(user_id=input.user_id)
    if user == None : return None

    logger.info("회원존재")

    # 회원비밀번호 검증
    if not security.verify_password(input.password, user.password) : return None

    # jwt토큰 발급
    jwt = security.create_access_token(data=user.__dict__)
    logger.info(jwt)

    userInfo = auth_schema.UserInfo(
        user_id=user.user_id,
        nickname=user.nickname,
        img_id=user.img_id
    )

    return (userInfo, jwt)
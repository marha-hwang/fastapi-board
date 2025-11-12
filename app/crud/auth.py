from app.schema.auth import LoginRequest, LoginResponse, User
from app.core.security import verify_password, create_access_token
import os  # 파일 존재 여부를 확인하기 위해 os 모듈 임포트
import logging
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA_FILE = os.path.join(BASE_DIR, "user_data.csv")

logging.basicConfig(
    level=logging.INFO,  # 로그 레벨을 INFO로 설정
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


async def verify_user(user:LoginRequest) -> LoginResponse:

    # 회원 검증 로직
    if not os.path.exists(USER_DATA_FILE): return None
    df = pd.read_csv(USER_DATA_FILE, encoding='utf-8')
    if df.query("user_id == @user.user_id").empty : return None

    hashed_password = df.query("user_id == @user.user_id")['password'].iloc[0]
    if not verify_password(user.password, hashed_password) : return None

    # jwt토큰 발급
    jwt = create_access_token(data=user.__dict__)
    logger.info(jwt)

    user = df.query("user_id == @user.user_id")
    user_response = User(user_id= user['user_id'].iloc[0],
                         nickname= user['nickname'].iloc[0],
                         img_id= user['img_id'].iloc[0])
    login_response = LoginResponse(access_token=jwt, token_type="bearer", user=user_response)

    return login_response

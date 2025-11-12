from app.schema.user import UserCreate, UserDelete, UserUpdate, UserPasswordChange
import pandas as pd
import os  # 파일 존재 여부를 확인하기 위해 os 모듈 임포트
import logging
from passlib.context import CryptContext
from app.core.security import get_password_hash
import app.model.user as model_user

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA_FILE = os.path.join(BASE_DIR, "user_data.csv")

logging.basicConfig(
    level=logging.INFO,  # 로그 레벨을 INFO로 설정
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


async def insert_user(user: UserCreate) :
        
    user_dict_list = [user.model_dump()]
    df = pd.DataFrame(user_dict_list)
    logger.info(f"{user_dict_list}")

    if not os.path.exists(USER_DATA_FILE):
        # 2-A. 파일이 없으면: 헤더와 함께 새로 쓰기
        df.to_csv(USER_DATA_FILE, index=False, encoding='utf-8-sig')
        return "회원가입이 성공적으로 완료되었습니다."
    
    # 2-B. 파일이 있으면: 헤더 없이(header=False),
    #                  추가 모드(mode='a')로 저장
    csv = pd.read_csv(USER_DATA_FILE, encoding='utf-8')
    logger.info(csv)
    if not csv.query("user_id == @user.user_id").empty : return "이미 등록된 사용자입니다."

    # 회원 추가 로직
    # 비밀번호 해싱
    logger.info(f"입력 비밀번호 : {user.password}")
    df['password'] = get_password_hash(user.password)
    df.to_csv(USER_DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')


    return "회원가입이 성공적으로 완료되었습니다."

async def delete_user(user: str) :
    

    if not os.path.exists(USER_DATA_FILE): return "존재하지 않는 회원입니다."
    
    csv = pd.read_csv(USER_DATA_FILE, encoding='utf-8')
    logger.info(csv)

    if csv.query("user_id == @user").empty :
        return "존재하지 않는 회원입니다."
    
    # 회원 삭제 로직
    df = csv.query(("user_id != @user"))
    df.to_csv(USER_DATA_FILE, header=True, index=False, encoding='utf-8-sig')

    return "회원 삭제가 성공적으로 완료되었습니다."

async def update_user(user: UserUpdate) :
    
    user_dict_list = [user.model_dump()]
    logger.info(f"{user_dict_list}")

    if not os.path.exists(USER_DATA_FILE): return "존재하지 않는 회원입니다."
    
    df = pd.read_csv(USER_DATA_FILE, encoding='utf-8')
    logger.info(df)

    if df.query("user_id == @user.user_id").empty :
        return "존재하지 않는 회원입니다."
    
    print(df.loc[df['user_id'] == user.user_id, ['nickname', 'img_id']])

    # 회원 업데이트 로직
    df.loc[df['user_id'] == user.user_id, ['nickname', 'img_id']] = [user.nickname, user.img_id]
    df.to_csv(USER_DATA_FILE, header=True, index=False, encoding='utf-8-sig')

    return "회원정보 업데이트가 성공적으로 완료되었습니다."

async def update_password(user: UserPasswordChange) :
    
    user_dict_list = [user.model_dump()]
    logger.info(f"{user_dict_list}")

    if not os.path.exists(USER_DATA_FILE): return "존재하지 않는 회원입니다."
    
    df = pd.read_csv(USER_DATA_FILE, encoding='utf-8')
    logger.info(df)

    if df.query("user_id == @user.user_id").empty :
        return "존재하지 않는 회원입니다."
    
    # 패스워드 업데이트 로직
    hashed_password = get_password_hash(user.new_password)

    df.loc[df['user_id'] == user.user_id, ['password']] = [hashed_password]
    df.to_csv(USER_DATA_FILE, header=True, index=False, encoding='utf-8-sig')

    return "패스워드 업데이트가 성공적으로 완료되었습니다."

import pandas as pd
import os
import logging
import app.config as config
import app.model.models as models

from sqlalchemy.orm import Session


BASE_DIR = config.db_path
USER_DATA_FILE = os.path.join(BASE_DIR, "user_data.csv")

logger = logging.getLogger(__name__)

dtype = {'user_id': str, 'password':str, 'nickname':str,'img_id':str}

def select_user(user_id:str)->models.User:
    if not os.path.exists(USER_DATA_FILE) : return None

    df = pd.read_csv(USER_DATA_FILE,
                     encoding='utf-8',
                     dtype=dtype)
    df = df.query("user_id == @user_id")
    if df.empty : return None

    return models.User( user_id= df['user_id'].iloc[0],
                 password=df['password'].iloc[0],
                 nickname= df['nickname'].iloc[0],
                 img_id= df['img_id'].iloc[0]
            )

def insert_user(user: models.User, db: Session)->bool :
        
     # 새 사용자 생성
    db.add(user)
    db.commit()
    db.refresh(user)

    # user_dict = [user.model_dump()]
    # df = pd.DataFrame(user_dict)
    # logger.info(f"{user_dict}")
    
    # # 2-A. 파일이 없으면: 헤더와 함께 새로 쓰기
    # if not os.path.exists(USER_DATA_FILE): df.to_csv(USER_DATA_FILE, index=False, encoding='utf-8-sig')    
    # # 2-B. 파일이 있으면: 헤더 없이(header=False), 추가 모드(mode='a')로 저장
    # else : df.to_csv(USER_DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')

    return True

def delete_user(user_id: str)->bool :
    
    df = pd.read_csv(USER_DATA_FILE,
                     encoding='utf-8',
                     dtype=dtype)
    df = df.query(("user_id != @user_id"))
    df.to_csv(USER_DATA_FILE, header=True, index=False, encoding='utf-8-sig')

    return True

def update_user(user: models.User) -> bool :
    
    df = pd.read_csv(USER_DATA_FILE,
                     encoding='utf-8',
                     dtype=dtype)
    df.loc[df['user_id'] == user.user_id, ['nickname', 'img_id']] = [user.nickname, user.img_id]
    df.to_csv(USER_DATA_FILE, header=True, index=False, encoding='utf-8-sig')

    return True

def update_password(new_password:str, user_id:str) :
    
    df = pd.read_csv(USER_DATA_FILE,
                     encoding='utf-8',
                     dtype=dtype)

    df.loc[df['user_id'] == user_id, ['password']] = [new_password]
    df.to_csv(USER_DATA_FILE, header=True, index=False, encoding='utf-8-sig')

    return True

def select_user_profile(user_id:str)->str:
    if not os.path.exists(USER_DATA_FILE) : return ""

    df = pd.read_csv(USER_DATA_FILE,
                     encoding='utf-8',
                     dtype=dtype)
    df = df.query("user_id == @user_id")
    if df.empty : return ""

    return df['img_id'].iloc[0]

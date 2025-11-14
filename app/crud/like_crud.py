import pandas as pd
import os
import logging
import app.config as config
import app.model.models as models

BASE_DIR = config.db_path
LIKE_DATA_FILE = os.path.join(BASE_DIR, "like_data.csv")

logger = logging.getLogger(__name__)

dtype = {'post_id': str, 'user_id': str}

def select_like(post_id:str, user_id:str):
    if not os.path.exists(LIKE_DATA_FILE) : return None

    logger.info(f"{post_id}, {user_id}")
    df = pd.read_csv(LIKE_DATA_FILE, 
                     encoding='utf-8', 
                     dtype=dtype)
    
    logger.info(df)
    df = df.query("(user_id == @user_id) & (post_id == @post_id)")
    logger.info(f"##########{df}")
    if df.empty : return None

    return models.Like(user_id=df['user_id'].iloc[0], post_id=df['post_id'].iloc[0])


def insert_like(post_id:str, user_id:str)->bool:
    df = pd.DataFrame([{"post_id": post_id, "user_id": user_id}])
    
    # 2-A. 파일이 없으면: 헤더와 함께 새로 쓰기
    if not os.path.exists(LIKE_DATA_FILE): df.to_csv(LIKE_DATA_FILE, index=False, encoding='utf-8-sig')    
    # 2-B. 파일이 있으면: 헤더 없이(header=False), 추가 모드(mode='a')로 저장
    else : df.to_csv(LIKE_DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')

    return True

def delete_like(post_id:str, user_id:str)->bool:
    df = pd.read_csv(LIKE_DATA_FILE, 
                     encoding='utf-8', 
                     dtype=dtype)
    df = df.query("(user_id != @user_id) | (post_id != @post_id)")
    df.to_csv(LIKE_DATA_FILE, header=True, index=False, encoding='utf-8-sig')

    return True

def select_like_cnt(post_id:str)->int:
    logger.info("select_like_cnt")
    if not os.path.exists(LIKE_DATA_FILE) : return 0

    df = pd.read_csv(LIKE_DATA_FILE, 
                     encoding='utf-8', 
                     dtype=dtype)
    df = df.query("post_id == @post_id")
    if df.empty : return 0

    return len(df)

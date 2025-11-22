import pandas as pd
import os
import logging
import app.config as config
import app.model.models as models
from app.repository.base_comment_repository import BaseCommentRepository

BASE_DIR = config.csv_data_path
COMMENT_DATA_FILE = os.path.join(BASE_DIR, "comment_data.csv")

logger = logging.getLogger(__name__)

dtype = {'comment_id': str, 'post_id': str, 'user_id':str, 'content':str, 'create_time':str}

class CommentRepositoryCSV(BaseCommentRepository) :

    def select_comment(self, comment_id:str)->models.Comment:
        if not os.path.exists(COMMENT_DATA_FILE) : return None

        df = pd.read_csv(COMMENT_DATA_FILE,
                        encoding='utf-8',
                        dtype=dtype)
        df = df.query("comment_id == @comment_id")
        if df.empty : return None

        return models.Comment( 
                    comment_id=df['comment_id'].iloc[0],
                    post_id=df['post_id'].iloc[0],
                    user_id=df['user_id'].iloc[0],
                    content=df['content'].iloc[0],
                    create_time=df['create_time'].iloc[0]
                )

    def insert_comment(self, comment:models.Comment):
        comment_dict = [{col.name: getattr(comment, col.name) for col in comment.__table__.columns}]
        df = pd.DataFrame(comment_dict)
        logger.info(f"{comment_dict}")
        
        # 2-A. 파일이 없으면: 헤더와 함께 새로 쓰기
        if not os.path.exists(COMMENT_DATA_FILE): df.to_csv(COMMENT_DATA_FILE, index=False, encoding='utf-8-sig')    
        # 2-B. 파일이 있으면: 헤더 없이(header=False), 추가 모드(mode='a')로 저장
        else : df.to_csv(COMMENT_DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')



    def delete_comment(self, comment_id:str):

        if not os.path.exists(COMMENT_DATA_FILE): return False

        df = pd.read_csv(COMMENT_DATA_FILE,
                        encoding='utf-8',
                        dtype=dtype)
        df = df.query(("comment_id != @comment_id"))
        df.to_csv(COMMENT_DATA_FILE, header=True, index=False, encoding='utf-8-sig')



    def update_comment(self, comment:models.Comment):

        if not os.path.exists(COMMENT_DATA_FILE): return False

        df = pd.read_csv(COMMENT_DATA_FILE,
                        encoding='utf-8',
                        dtype=dtype)
        df.loc[df['comment_id'] == comment.comment_id, ['content']] = [comment.content]
        df.to_csv(COMMENT_DATA_FILE, header=True, index=False, encoding='utf-8-sig')


    def select_comment_list(self, post_id:str)->list[models.Comment]:
        if not os.path.exists(COMMENT_DATA_FILE) : return None

        df = pd.read_csv(COMMENT_DATA_FILE,
                        encoding='utf-8',
                        dtype=dtype)
        df = df.query("post_id == @post_id")
        if df.empty : return None

        comment_list:list[models.Comment] = []

        # df의 모든 요소를 반복
        for index, row in df.iterrows() :

            # comment 구성
            comment = models.Comment(         
                comment_id=row['comment_id'],
                post_id=row['post_id'],
                user_id=row['user_id'],
                content=row['content'],
                create_time=row['create_time']
            )

            #배열에 추가
            comment_list.append(comment)
            
        return comment_list

    def select_comment_cnt(self, post_id:str)->int:
        if not os.path.exists(COMMENT_DATA_FILE) : return 0

        df = pd.read_csv(COMMENT_DATA_FILE, encoding='utf-8')
        df = df.query("post_id == @post_id")
        if df.empty : return 0

        return len(df)

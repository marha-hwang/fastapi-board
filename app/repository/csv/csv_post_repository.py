import pandas as pd
import os
import logging
import app.config as config
import app.model.models as models
from app.repository.base_post_repository import BasePostRepository

BASE_DIR = config.csv_data_path
POST_DATA_FILE = os.path.join(BASE_DIR, "post_data.csv")

logger = logging.getLogger(__name__)

dtype = {'post_id': str, 'user_id': str, 'title':str, 'content':str, 
              'img_id':str, 'view_cnt':int, 'create_time':str}

class PostRepositoryCSV(BasePostRepository) :

    def select_post(self, post_id:str)->models.Post:
        if not os.path.exists(POST_DATA_FILE) : return None

        df = pd.read_csv(POST_DATA_FILE,
                        encoding='utf-8',
                        dtype=dtype)
        df = df.query("post_id == @post_id")
        if df.empty : return None

        return models.Post( 
                post_id=df['post_id'].iloc[0],
                user_id=df['user_id'].iloc[0],
                title=df['title'].iloc[0],
                content=df['content'].iloc[0],
                img_id=df['img_id'].iloc[0],
                view_cnt=df['view_cnt'].iloc[0],
                create_time=df['create_time'].iloc[0]
            )

    def insert_post(self, post:models.Post):
        post_dict = [{col.name: getattr(post, col.name) for col in post.__table__.columns}]
        df = pd.DataFrame(post_dict)
        logger.info(f"{post_dict}")
        
        # 2-A. 파일이 없으면: 헤더와 함께 새로 쓰기
        if not os.path.exists(POST_DATA_FILE): df.to_csv(POST_DATA_FILE, index=False, encoding='utf-8-sig')    
        # 2-B. 파일이 있으면: 헤더 없이(header=False), 추가 모드(mode='a')로 저장
        else : df.to_csv(POST_DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')

    def delete_post(self, post_id:str):

        if not os.path.exists(POST_DATA_FILE): return False

        df = pd.read_csv(POST_DATA_FILE,
                        encoding='utf-8',
                        dtype=dtype)
        df = df.query(("post_id != @post_id"))
        df.to_csv(POST_DATA_FILE, header=True, index=False, encoding='utf-8-sig')

    def update_post(self, post:models.Post):

        if not os.path.exists(POST_DATA_FILE): return False

        df = pd.read_csv(POST_DATA_FILE,
                        encoding='utf-8',
                        dtype=dtype)
        df.loc[df['post_id'] == post.post_id, ['title', 'content', 'img_id']] = [post.title, post.content, post.img_id]
        df.to_csv(POST_DATA_FILE, header=True, index=False, encoding='utf-8-sig')

    def increase_view_post_cnt(self, post_id:str):

        if not os.path.exists(POST_DATA_FILE): return False

        df = pd.read_csv(POST_DATA_FILE,
                        encoding='utf-8',
                        dtype=dtype)
        df.loc[df['post_id'] == post_id, 'view_cnt'] = df.loc[df['post_id'] == post_id, 'view_cnt'] + 1
        df.to_csv(POST_DATA_FILE, header=True, index=False, encoding='utf-8-sig')

    def select_post_all(self)->list[models.Post]:

        if not os.path.exists(POST_DATA_FILE): return None

        df = pd.read_csv(POST_DATA_FILE,
                        encoding='utf-8',
                        dtype=dtype)
        if df.empty : return None

        post_list:list[models.Post] = []

        # df의 모든 요소를 반복
        for index, row in df.iterrows() :
            # PostList구성
            post = models.Post(
                post_id=row['post_id'],
                user_id=row['user_id'],
                title=row['title'],
                content=row['content'],
                img_id=row['img_id'],
                view_cnt=row['view_cnt'],
                create_time=row['create_time'],
            )

            #배열에 추가
            post_list.append(post)
            
        return post_list


    # def select_post_detail(post_id:str, user_id:str)->post_schema.PostDetailRes:

    #     if not os.path.exists(POST_DATA_FILE): return None

    #     df = pd.read_csv(POST_DATA_FILE,
    #                     encoding='utf-8',
    #                     dtype=dtype)
    #     df = df.query("post_id == @post_id")
    #     if df.empty : return None

    #     profile_id = user_crud.select_user_profile(user_id=user_id)
    #     like_cnt = like_crud.select_like_cnt(post_id=post_id)
    #     like_YN = 'Y' if like_crud.select_like(post_id=post_id, user_id=user_id) else 'N'
    #     comment_cnt = comment_crud.select_comment_cnt(post_id=post_id)

    #     logger.info(f"######user_id : {user_id}, post_id : {post_id}")
    #     logger.info(f"profile : {profile_id}, like_cnt : {like_cnt}, like_YN : {like_YN}, comment_cnt : {comment_cnt}")

    #     row = df.iloc[0]


    #     # PostList구성
    #     post = post_schema.PostDetailRes(
    #         post_id=row['post_id'],
    #         title=row['title'],
    #         content=row['content'],
    #         user_id=row['user_id'],
    #         profile_id=profile_id,
    #         img_id=row['img_id'],
    #         like_cnt=like_cnt,
    #         comment_cnt=comment_cnt,
    #         view_cnt=row['view_cnt'],
    #         create_time=row['create_time'],
    #         like_YN=like_YN
    #     )

    #     return post
        
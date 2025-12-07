import pandas as pd
import os
import logging
import app.config as config
import app.model.models as models
from app.repository.base_file_repository import BaseFileRepository

BASE_DIR = config.csv_data_path
FILE_DATA_FILE = os.path.join(BASE_DIR, "file_data.csv")

logger = logging.getLogger(__name__)

dtype = {'img_id': str, 'img_url': str}

class FileRepositoryCSV(BaseFileRepository) :

    def select_file(self, img_id:str)->models.File:
        if not os.path.exists(FILE_DATA_FILE) : return None

        df = pd.read_csv(FILE_DATA_FILE, 
                        encoding='utf-8', 
                        dtype=dtype)
        
        logger.info(df)
        df = df.query("(img_id == @img_id)")
        logger.info(f"##########{df}")
        if df.empty : return None

        return models.File(img_id=df['img_id'].iloc[0], img_url=df['img_url'].iloc[0])


    def insert_file(self, file:models.File):
        df = pd.DataFrame([{"img_id": file.img_id, "img_url": file.img_url}])
        
        # 2-A. 파일이 없으면: 헤더와 함께 새로 쓰기
        if not os.path.exists(FILE_DATA_FILE): df.to_csv(FILE_DATA_FILE, index=False, encoding='utf-8-sig')    
        # 2-B. 파일이 있으면: 헤더 없이(header=False), 추가 모드(mode='a')로 저장
        else : df.to_csv(FILE_DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')

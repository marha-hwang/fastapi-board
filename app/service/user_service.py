import app.schema.user_schema as user_schema
import app.model.models as app_models
import app.core.security as security
import app.crud.user_crud as user_crud
import logging
import pandas as pd

from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

def create_user(input: user_schema.UserCreate, db:Session)->str :

    if user_crud.select_user(user_id=input.user_id) != None : return "이미 등록된 사용자입니다."

    hashedPassword = security.get_password_hash(input.password)
    user = app_models.User(
        user_id=input.user_id,
        password=hashedPassword,
        nickname=input.nickname,
        img_id=input.img_id
    )
    
    if user_crud.insert_user(user=user, db=db) : return "회원가입이 성공적으로 완료되었습니다."
    else : return "회원가입에 실패하였습니다."

def remove_user(user_id:str)->str :
    if user_crud.select_user(user_id=user_id) == None : return "등록되지 않은 사용자입니다."

    if user_crud.delete_user(user_id=user_id) : return "회원 삭제가 성공적으로 완료되었습니다."
    else : return "회원삭제에 실패하였습니다."

def update_user(input:user_schema.UserUpdate, user_id:str)->str :
    
    if user_crud.select_user(user_id=user_id) == None : "등록되지 않은 사용자입니다."

    user = app_models.User(
        user_id=user_id,
        password="",
        nickname=input.nickname,
        img_id=input.img_id
    )

    if user_crud.update_user(user=user) : return "회원 업데이트가 성공적으로 완료되었습니다."
    else : return "회원 업데이트에 실패하였습니다."


def update_password(input:user_schema.UserPasswordChange, user_id:str)->str :

    if user_crud.select_user(user_id=user_id) == None : "등록되지 않은 사용자입니다."

    hashedPassword = security.get_password_hash(input.new_password)
    if user_crud.update_password(new_password=hashedPassword, user_id=user_id) : return "비밀번호 업데이트가 성공적으로 완료되었습니다."
    else : return "비밀번호 업데이트에 실패하였습니다."


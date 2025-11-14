from pydantic import BaseModel


#1. Payload 1: 회원 가입 (모든 정보 포함)
# user_id, password, nickname, img_id
class UserCreate(BaseModel):
    user_id: str
    password: str
    nickname: str
    img_id: str

# 2. Payload 2: 사용자 식별 (ID만 포함)
# (예: 사용자 조회, 탈퇴, 단순 식별 등)
class UserDelete(BaseModel):
    user_id: str

# 3. Payload 3: 사용자 정보 수정 (비밀번호 제외)
# user_id, nickname, img_id
class UserUpdate(BaseModel):
    nickname: str
    img_id: str

# 4. Payload 4: 비밀번호 변경
# user_id, new_password
class UserPasswordChange(BaseModel):
    new_password: str
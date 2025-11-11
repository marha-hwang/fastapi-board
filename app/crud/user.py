from app.schema.user import UserCreate, UserDelete, UserUpdate, UserPasswordChange
import pandas as pd

def create_user(user: UserCreate) :
    df = pd.DataFrame(user)
    df.to_csv("user_data.csv")
from fastapi import Depends
from sqlalchemy.orm import Session
from pydantic import EmailStr


from core.database import get_db
from core.security import hash_password
from schemas import UserRegistrationSchema
from models import Users


class UsersRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        
    def create(self, new_user: UserRegistrationSchema):
        user_dict = new_user.model_dump()
        user_dict["hashed_password"] = hash_password(new_user.password)
        user_dict.pop("password")
        db_user = Users(**user_dict)
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user
    
    def get_by_username(self, username: str):
        return self.db.query(Users).filter(Users.username == username).first()
    
    def get_by_id(self, id: int):
        return self.db.query(Users).filter(Users.id == id).first()
    
    def get_by_email(self, email: str | EmailStr):
        return self.db.query(Users).filter(Users.email == email).first()
from repositories import UsersRepository
from fastapi import Depends, HTTPException

from schemas import UserRegistrationSchema, UserLoginSchema, AccessTokenSchema
from core.security import verify_password, create_access_token


class UsersService:
    def __init__(self, repository: UsersRepository = Depends()):
        self.repo = repository
    
    async def create_user(self, user: UserRegistrationSchema):
        if not await self.repo.get_by_username(user.username) and not await self.repo.get_by_email(user.email):
            db_user = await self.repo.create(user)
            
            return db_user
        
        else:
            raise HTTPException(status_code=400, detail="Пользователь уже существует")
        
    async def get_user_by_username(self, username: str):
        db_user = await self.repo.get_by_username(username)
        if not db_user:
            raise HTTPException(status_code=404, detail="Пользователь не существует")
        
        return db_user
    
    async def authenticate_user(self, credentials: UserLoginSchema):
        db_user = await self.get_user_by_username(credentials.username)
        
        if not await verify_password(credentials.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Не верные данные входа")
        
        token = await create_access_token({
            "sub": db_user.username,
        })
        
        return AccessTokenSchema(access_token=token, token_type="bearer")

from pydantic import BaseModel, EmailStr, Field


class UserRegistrationSchema(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    email: EmailStr = Field(min_length=4, max_length=50)
    password: str


class UserInfoSchema(BaseModel):
    id: int
    username: str
    email: str


class UserLoginSchema(BaseModel):
    username: str
    password: str


class AccessTokenSchema(BaseModel):
    access_token: str
    token_type: str


class AccessTokenSchema(BaseModel):
    access_token: str
    token_type: str
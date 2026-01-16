from pydantic import BaseModel, Field
import uuid


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=72)


class UserLogin(BaseModel):
    username: str = Field(max_length=30)
    password: str = Field(max_length=72)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: uuid.UUID | None = None


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str

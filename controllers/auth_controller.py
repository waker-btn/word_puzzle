from datetime import timedelta
from fastapi import HTTPException, status
from sqlmodel import Session, select
from models.db import Users
from schemas.auth import UserRegister, UserLogin, Token, UserResponse
from utils.auth import hash_password, verify_password, create_access_token
from settings import settings


def register_user(user_data: UserRegister, session: Session) -> UserResponse:
    # Check if user already exists
    existing_user = session.exec(
        select(Users).where(Users.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Create new user with hashed password
    hashed_pw = hash_password(user_data.password)
    new_user = Users(username=user_data.username, password=hashed_pw)

    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user",
        )

    return UserResponse(id=new_user.id, username=new_user.username)


def login_user(user_data: UserLogin, session: Session) -> Token:
    # Find user by username
    user = session.exec(
        select(Users).where(Users.username == user_data.username)
    ).first()

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")

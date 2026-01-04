from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from database import get_session
from models.db import Users
from utils.auth import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Get current authenticated user from JWT token
def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> Users:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = verify_access_token(token)
    if user_id is None:
        raise credentials_exception

    user = session.exec(select(Users).where(Users.id == user_id)).first()
    if user is None:
        raise credentials_exception

    return user

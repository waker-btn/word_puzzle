from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlmodel import Session
from schemas.games import GuessRequest, GameResponse, GuessResponse
from schemas.auth import UserRegister, UserLogin, AccessToken, UserResponse
from controllers.games_controller import (
    get_today_game,
    make_guess as make_guess_controller,
)
from controllers.auth_controller import register_user, login_user, refresh_access_token
from database import get_session
from dependencies.auth import get_current_user
from models.db import Users
from settings import settings

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    """Check API health status"""
    return {"status": "ok"}


@router.post("/register", response_model=UserResponse, tags=["Authentication"])
def register(user_data: UserRegister, session: Session = Depends(get_session)):
    """Register a new user account"""
    return register_user(user_data, session)


@router.post("/login", response_model=AccessToken, tags=["Authentication"])
def login(
    user_data: UserLogin, response: Response, session: Session = Depends(get_session)
):
    """Login and receive an access token"""
    result = login_user(user_data, session)

    # Set cookie for cross-origin (Vercel <-> Railway)
    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,  # Prevents JavaScript access
        secure=True,  # Required for samesite=none
        samesite="none",  # Required for cross-origin
        max_age=7 * 24 * 60 * 60,  # 7 days in seconds
    )

    return AccessToken(access_token=result.access_token)


@router.post("/refresh-token", response_model=AccessToken, tags=["Authentication"])
def refresh_token(refresh_token: str = Cookie(None)):
    """Refresh access token using refresh token from cookie"""
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    new_access_token = refresh_access_token(refresh_token)
    return new_access_token


@router.post("/logout", tags=["Authentication"])
def logout(response: Response):
    """Logout user by clearing the refresh token cookie"""
    response.delete_cookie(
        key="refresh_token",
        secure=True,
        samesite="none"
    )
    return {"detail": "Logged out successfully"}


@router.get("/games/words", tags=["Game"])
def get_game(
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
) -> GameResponse:
    """Get or start today's word puzzle game"""
    return get_today_game(current_user.id, session)


@router.post("/games/words", response_model=GuessResponse, tags=["Game"])
def make_guess(
    guess_request: GuessRequest,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """Submit a guess for today's word puzzle"""
    return make_guess_controller(guess_request.guess, current_user.id, session)

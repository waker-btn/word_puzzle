from fastapi import APIRouter, Depends
from sqlmodel import Session
from schemas.games import GuessRequest, GameResponse
from schemas.auth import UserRegister, UserLogin, Token, UserResponse
from controllers.games_controller import (
    get_today_game,
    make_guess as make_guess_controller,
)
from controllers.auth_controller import register_user, login_user
from database import get_session
from dependencies.auth import get_current_user
from models.db import Users

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    """Check API health status"""
    return {"status": "ok"}


@router.post("/register", response_model=UserResponse, tags=["Authentication"])
def register(user_data: UserRegister, session: Session = Depends(get_session)):
    """Register a new user account"""
    return register_user(user_data, session)


@router.post("/login", response_model=Token, tags=["Authentication"])
def login(user_data: UserLogin, session: Session = Depends(get_session)):
    """Login and receive an access token"""
    return login_user(user_data, session)


@router.get("/games/words", tags=["Game"])
def get_game(
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
) -> GameResponse:
    """Get or start today's word puzzle game"""
    return get_today_game(current_user.id, session)


@router.post("/games/words", tags=["Game"])
def make_guess(
    guess_request: GuessRequest,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    """Submit a guess for today's word puzzle"""
    return make_guess_controller(guess_request.guess, current_user.id, session)

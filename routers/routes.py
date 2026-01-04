from fastapi import APIRouter, Depends
from sqlmodel import Session
from schemas.games import GuessRequest, NewGameResponse
from schemas.auth import UserRegister, UserLogin, Token, UserResponse
from controllers.games_controller import (
    start_game as start_game_controller,
    make_guess as make_guess_controller,
)
from controllers.auth_controller import register_user, login_user
from database import get_session
from dependencies.auth import get_current_user
from models.db import Users

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, session: Session = Depends(get_session)):
    return register_user(user_data, session)


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, session: Session = Depends(get_session)):
    return login_user(user_data, session)


@router.post("/games")
def start_game(
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
) -> NewGameResponse:
    return start_game_controller(current_user.id, session)


@router.post("/games/{game_id}")
def make_guess(
    game_id: str,
    guess_request: GuessRequest,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    return make_guess_controller(game_id, guess_request.guess, current_user.id, session)

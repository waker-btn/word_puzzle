from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from schemas.games import NewGameRequest, GuessRequest, NewGameResponse
from controllers.games_controller import (
    start_game as start_game_controller,
    make_guess as make_guess_controller,
)
from database import get_session

router = APIRouter()


@router.get("/health")
async def health_check(request: Request):
    return {"status": "ok"}


@router.post("/games")
def start_game(
    new_game_request: NewGameRequest, session: Session = Depends(get_session)
) -> NewGameResponse:
    return start_game_controller(new_game_request, session)


@router.post("/games/{game_id}/")
async def make_guess(
    game_id: str, guess_request: GuessRequest, session: Session = Depends(get_session)
):
    return make_guess_controller(game_id, guess_request, session)

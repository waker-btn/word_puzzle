from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/game/{attempt_word}")
async def make_attempt(request: Request, attempt_word: str):
    request.app.state.game_manager.active_game.make_attempt(attempt_word)
    return request.app.state.game_manager.send_game_state()

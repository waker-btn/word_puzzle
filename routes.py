from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/game/history")
async def get_game_state(request: Request):
    game_manager = request.app.state.game_manager
    return {"game_history": game_manager.game_history}


@router.post("/game/attempt")
async def make_attempt(request: Request, body: dict):
    game_manager = request.app.state.game_manager
    if game_manager.active_game is None:
        await game_manager.start_new_game()
    game_manager.active_game.make_attempt(body["word"])
    return game_manager.send_game_state()

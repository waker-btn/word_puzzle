from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import router
from game_service import game_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await game_manager.start_new_game()
    yield


app = FastAPI(lifespan=lifespan)
app.state.game_manager = game_manager
app.include_router(router)

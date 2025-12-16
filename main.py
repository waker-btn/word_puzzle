from fastapi import FastAPI
from routes import router
from game_service import game_manager


app = FastAPI()
app.state.game_manager = game_manager
app.include_router(router)

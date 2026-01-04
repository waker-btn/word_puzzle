from pydantic import BaseModel, Field
import uuid

from models.db import GameStatus


class NewGameRequest(BaseModel):
    user_id: uuid.UUID


class GuessRequest(BaseModel):
    guess: str = Field(max_length=5, min_length=5)
    user_id: uuid.UUID


class NewGameResponse(BaseModel):
    game_id: uuid.UUID
    remaining_attempts: int
    game_status: GameStatus


class GuessResponse(BaseModel):
    remaining_attempts: int
    game_status: GameStatus
    game_id: uuid.UUID
    attempt: list[str] = Field(default_factory=list, max_length=5)
    attempts: list[list[str]] = Field(default_factory=list)

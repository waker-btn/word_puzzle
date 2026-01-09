from pydantic import BaseModel, Field
import uuid

from models.db import GameStatus


class GuessRequest(BaseModel):
    guess: str = Field(max_length=5, min_length=5)


class GameResponse(BaseModel):
    game_id: uuid.UUID
    remaining_attempts: int
    game_status: GameStatus


class GuessResponse(BaseModel):
    remaining_attempts: int
    game_status: GameStatus
    game_id: uuid.UUID
    attempt: list[str] = Field(default_factory=list, max_length=5)
    attempts: list[list[str]] = Field(default_factory=list)
    word: str | None = None  # Included only if the game is won or lost

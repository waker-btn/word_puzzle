from pydantic import BaseModel


class Game(BaseModel):
    target_word: str
    letters: list[str]
    attempts: int
    max_attempts: int


class GameManager(BaseModel):
    game_history: list[Game] = []
    active_game: Game

import requests
from typing import Optional


class GameManager:
    def __init__(self):
        self.game_history = []
        self.active_game: Optional[Game] = None

    async def start_new_game(self):
        self.active_game = Game()
        await self.active_game.initialize()

    def end_active_game(self):
        self.game_history.append(self.active_game)
        self.active_game = None

    def send_game_state(self):
        if self.active_game is None:
            raise ValueError("No active game")
        response = {
            "game_state": self.active_game.game_state,
            "response_history": self.active_game.response_history,
        }
        if self.active_game.game_end:
            self.end_active_game()

        return response


class Game:
    def __init__(self):
        self.target_word: Optional[str] = None
        self.letters: list[str] = []
        self.attempts: int = 0
        self.max_attempts: int = 6
        self.game_state: str = "active"
        self.response_history: list[list[int]] = []
        self.game_end: bool = False

    async def initialize(self) -> None:
        response = requests.get(
            "https://random-word-api.herokuapp.com/word?number=1&length=5"
        ).json()[0]
        self.target_word = response
        self.letters = list(response)

    def make_attempt(self, attempt_word: str) -> None:
        response: list[int] = []
        for i, letter in enumerate(list(attempt_word)):
            if letter == self.letters[i]:
                response.append(2)
            elif letter in self.letters:
                response.append(1)
            else:
                response.append(0)
        self.update_game_state(response)

    def update_game_state(self, response: list[int]) -> None:
        self.attempts += 1
        self.response_history.append(response)
        if all(r == 2 for r in response):
            # Player has won
            self.game_state = "won"
            self.game_end = True
        elif self.attempts >= self.max_attempts:
            # Player has lost
            self.game_state = "lost"
            self.game_end = True


game_manager = GameManager()

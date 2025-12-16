import requests


class GameManager:
    def __init__(self):
        self.game_history = []
        self.active_game = Game()

    def end_active_game(self):
        self.game_history.append(self.active_game)
        self.active_game = Game()

    def send_game_state(self):
        response = {
            "game_state": self.active_game.game_state,
            "response_history": self.active_game.response_history,
        }
        if self.active_game.game_end:
            self.end_active_game()

        return response


game_manager = GameManager()


class Game:
    async def __init__(self):
        self.target_word = requests.get(
            "https://random-word-api.herokuapp.com/word?number=1&length=5"
        ).json()[0]
        self.letters = list(self.target_word)
        self.attempts = 0
        self.max_attempts = 6
        self.game_state = "active"
        self.response_history = []
        self.game_end = False

    def make_attempt(self, attempt_word: str):
        response = []
        for i, letter in enumerate(list(attempt_word)):
            if letter == self.letters[i]:
                response.append(2)
            elif letter in self.letters:
                response.append(1)
            else:
                response.append(0)
        self.update_game_state(response)

    def update_game_state(self, response: list[int]):
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

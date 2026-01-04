from schemas.games import NewGameRequest, NewGameResponse, GuessRequest, GuessResponse
from fastapi import Depends, HTTPException
from sqlmodel import Session, func, select
from database import get_session
from models.db import Games, Words, GameStatus


def get_random_word(session: Session) -> str:
    with session:
        word = session.exec(select(Words).order_by(func.random())).first()
        return word.word if word else "apple"


def start_game(new_game_request: NewGameRequest, session: Session) -> NewGameResponse:
    new_game = Games(user_id=new_game_request.user_id, word=get_random_word(session))
    session.add(new_game)
    session.commit()
    session.refresh(new_game)

    return NewGameResponse(
        game_id=new_game.id,
        remaining_attempts=new_game.remaining_attempts,
        game_status=new_game.game_status,
    )


def make_guess(
    game_id: str, guess_request: GuessRequest, session: Session
) -> GuessResponse:

    if len(guess_request.guess) != 5:
        raise HTTPException(status_code=400, detail="Guess must be 5 characters")

    # get the word
    game = session.exec(select(Games).where(Games.id == game_id)).first()

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.game_status != "ongoing":
        raise HTTPException(status_code=400, detail="Game is not ongoing")

    # check the guess
    guess_array = list(guess_request.guess.lower())
    game_array = list(game.word.lower())
    attempt = ""

    for guess_char, game_char in zip(guess_array, game_array):
        if guess_char == game_char:
            # correct position
            attempt += "2"
        elif guess_char in game_array:
            # wrong position
            attempt += "1"
        else:
            # not in word
            attempt += "0"

    # create attempt
    game.attempts = game.attempts + [[guess_request.guess, attempt]]

    # update game status
    # check win/loss
    game.remaining_attempts -= 1
    if attempt == "22222":
        game.game_status = GameStatus.won
    elif game.remaining_attempts == 0:
        game.game_status = GameStatus.lost

    # update db
    session.add(game)
    session.commit()
    session.refresh(game)

    return GuessResponse(
        remaining_attempts=game.remaining_attempts,
        game_status=game.game_status,
        game_id=game.id,
        attempt=game.attempts[-1],
        attempts=game.attempts,
    )

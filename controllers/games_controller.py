from fastapi import HTTPException
from sqlmodel import Session, func, select
from models.db import Games, Words, GameStatus
from schemas.games import NewGameResponse, GuessResponse
import uuid


def get_random_word(session: Session) -> str:
    with session:
        word = session.exec(select(Words).order_by(func.random())).first()
        return word.word if word else "apple"


def start_game(user_id: uuid.UUID, session: Session) -> NewGameResponse:
    new_game = Games(user_id=user_id, word=get_random_word(session))
    session.add(new_game)
    session.commit()
    session.refresh(new_game)

    return NewGameResponse(
        game_id=new_game.id,
        remaining_attempts=new_game.remaining_attempts,
        game_status=new_game.game_status,
    )


def make_guess(
    game_id: str, guess: str, user_id: uuid.UUID, session: Session
) -> GuessResponse:

    if len(guess) != 5:
        raise HTTPException(status_code=400, detail="Guess must be 5 characters")

    # Get the game
    game = session.exec(select(Games).where(Games.id == game_id)).first()

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to play this game")

    if game.game_status != "ongoing":
        raise HTTPException(status_code=400, detail="Game is not ongoing")

    # Check the guess
    guess_array = list(guess.lower())
    game_array = list(game.word.lower())
    attempt = ""

    for guess_char, game_char in zip(guess_array, game_array):
        if guess_char == game_char:
            attempt += "2"  # Correct position
        elif guess_char in game_array:
            attempt += "1"  # Wrong position
        else:
            attempt += "0"  # Not in word

    # Store attempt
    game.attempts = game.attempts + [[guess, attempt]]

    # Update game status
    game.remaining_attempts -= 1
    if attempt == "22222":
        game.game_status = GameStatus.won
    elif game.remaining_attempts == 0:
        game.game_status = GameStatus.lost

    # Save to database
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

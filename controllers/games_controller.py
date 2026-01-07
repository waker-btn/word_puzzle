from fastapi import HTTPException
from sqlmodel import Session, func, select
from models.db import Games, Words, GameStatus
from schemas.games import NewGameResponse, GuessResponse
import uuid


def get_random_word(session: Session) -> str:
    with session:
        word = session.exec(select(Words).order_by(func.random())).first()
        if not word:
            raise HTTPException(
                status_code=500,
                detail="No words available in database. Please contact administrator.",
            )
        return word.word


def start_game(user_id: uuid.UUID, session: Session) -> NewGameResponse:
    try:
        new_game = Games(user_id=user_id, word=get_random_word(session))
        session.add(new_game)
        session.commit()
        session.refresh(new_game)

        return NewGameResponse(
            game_id=new_game.id,
            remaining_attempts=new_game.remaining_attempts,
            game_status=new_game.game_status,
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to create game")


def make_guess(
    game_id: str, guess: str, user_id: uuid.UUID, session: Session
) -> GuessResponse:

    if len(guess) != 5:
        raise HTTPException(status_code=400, detail="Guess must be 5 characters")

    if not guess.isalpha():
        raise HTTPException(status_code=400, detail="Guess must contain only letters")

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
    attempt = ["0"] * 5
    remaining_letters = list(game.word.lower())

    # First pass: mark correct positions (2s)
    for i, (guess_char, game_char) in enumerate(zip(guess_array, game_array)):
        if guess_char == game_char:
            attempt[i] = "2"
            remaining_letters[i] = ""  # Mark this letter as used

    # Second pass: mark wrong positions (1s)
    for i, guess_char in enumerate(guess_array):
        if attempt[i] == "0":  # Not already marked as correct
            if guess_char in remaining_letters:
                attempt[i] = "1"
                # Remove the first occurrence of this letter from remaining
                remaining_letters[remaining_letters.index(guess_char)] = ""

    attempt = "".join(attempt)

    # Store attempt
    game.attempts = game.attempts + [[guess, attempt]]

    # Update game status
    game.remaining_attempts -= 1
    if attempt == "22222":
        game.game_status = GameStatus.won
    elif game.remaining_attempts == 0:
        game.game_status = GameStatus.lost

    # Save to database
    try:
        session.add(game)
        session.commit()
        session.refresh(game)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to save game state")

    return GuessResponse(
        remaining_attempts=game.remaining_attempts,
        game_status=game.game_status,
        game_id=game.id,
        attempt=game.attempts[-1],
        attempts=game.attempts,
    )

from datetime import date
from fastapi import HTTPException
from sqlmodel import Session, func, select
from models.db import Games, Words, GameStatus
from schemas.games import GameResponse, GuessResponse
import uuid


def get_today_game(user_id: uuid.UUID, session: Session) -> GameResponse:
    today = date.today()
    today_game = session.exec(
        select(Games).where(Games.date == today).where(Games.user_id == user_id)
    ).first()
    if today_game:
        return GameResponse(
            game_id=today_game.id,
            remaining_attempts=today_game.remaining_attempts,
            game_status=today_game.game_status,
        )
    return start_game(user_id, session, today)


def start_game(user_id: uuid.UUID, session: Session, date_today: date) -> GameResponse:
    try:
        today_word = session.exec(select(Words).where(Words.date == date_today)).first()
        if not today_word:
            raise HTTPException(
                status_code=404, detail=f"No word available for {date_today}"
            )
        new_game = Games(user_id=user_id, date=date_today, word=today_word.word)
        session.add(new_game)
        session.commit()
        session.refresh(new_game)

        return GameResponse(
            game_id=new_game.id,
            remaining_attempts=new_game.remaining_attempts,
            game_status=new_game.game_status,
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"Error creating game: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create game: {str(e)}")


def make_guess(guess: str, user_id: uuid.UUID, session: Session) -> GuessResponse:

    if len(guess) != 5:
        raise HTTPException(status_code=400, detail="Guess must be 5 characters")

    if not guess.isalpha():
        raise HTTPException(status_code=400, detail="Guess must contain only letters")

    valid_word = session.exec(select(Words).where(Words.word == guess.lower())).first()
    if not valid_word:
        raise HTTPException(status_code=400, detail="Not a valid word")

    # Get the game
    game = session.exec(
        select(Games).where(Games.date == date.today()).where(Games.user_id == user_id)
    ).first()

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="No game found for today. Please GET /games/words to start today's game first.",
        )

    if game.game_status != "ongoing":
        # Return current game state without processing guess
        return GuessResponse(
            remaining_attempts=game.remaining_attempts,
            game_status=game.game_status,
            game_id=game.id,
            attempt=game.attempts[-1] if game.attempts else ["", ""],
            attempts=game.attempts,
            word=game.word,
        )

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
        word=game.word if game.game_status != GameStatus.ongoing else "Unknown",
    )

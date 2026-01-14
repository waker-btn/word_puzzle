# Word Puzzle API

A Wordle-style daily word guessing game API built with FastAPI. Players get 6 attempts to guess a 5-letter word, with feedback after each guess.

**🌐 Live API:** https://word-puzzle.up.railway.app

**📚 API Documentation:** https://word-puzzle.up.railway.app/docs

## What it does

- Daily 5-letter word puzzle (new word each day)
- 6 attempts to guess the word
- Feedback system: `2` = correct position, `1` = wrong position, `0` = not in word
- User authentication with JWT
- Each user gets their own game progress tracked per day

## Tech Stack

- **FastAPI** - Python web framework
- **PostgreSQL** - Database
- **SQLModel** - ORM
- **JWT** - Authentication
- **Uvicorn** - ASGI server

## Setup

### 1. Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Required variables:

```env
APP_ENV=development
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_USER=your_user
DATABASE_PW=your_password
DATABASE_NAME=word_puzzle

JWT_SECRET_KEY=your-secret-key  # Run: openssl rand -hex 32
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
RATE_LIMIT=10/minute
```

### 2. Install Dependencies

Using Poetry:

```bash
poetry install
poetry shell
```

### 3. Set Up PostgreSQL

Create an empty database:

```bash
createdb word_puzzle
```

The app will automatically create all the tables when it starts up.

### 4. Run the App

```bash
uvicorn main:app --reload
```

API will be at `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

## API Examples

### Register

```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Login

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

Returns: `{"access_token": "...", "token_type": "bearer"}`

### Start Today's Game

```bash
curl -X GET http://localhost:8000/games/words \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Make a Guess

```bash
curl -X POST http://localhost:8000/games/words \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"guess": "crane"}'
```

Response includes:

- `attempt`: Your guess and the feedback (e.g., `["crane", "01220"]`)
- `remaining_attempts`: How many guesses left
- `game_status`: `ongoing`, `won`, or `lost`
- `word`: The answer (only shown when game is over)

## How the Feedback Works

Each guess returns a 5-character string:

- `2` = Letter is correct and in the right spot (🟩)
- `1` = Letter is in the word but wrong spot (🟨)
- `0` = Letter is not in the word (⬜)

Example: If the word is "SWEET" and you guess "STALE":

- Result: `"21001"`
- S=2 (correct!), T=1 (in word, wrong spot), A=0 (not in word), L=0, E=1 (in word, wrong spot)

## Project Structure

```
word_puzzle/
├── main.py              # App entry point
├── database.py          # DB setup
├── settings.py          # Config
├── controllers/         # Business logic
├── models/              # Database models
├── routers/             # API routes
├── schemas/             # Request/response schemas
├── dependencies/        # Auth dependencies
└── utils/               # Helper functions
```

## Attributions

- Inspired by [Wordle](https://www.nytimes.com/games/wordle/index.html) by Josh Wardle
- Word list from [Random Word API](https://random-word-api.herokuapp.com/)
- Built by Matt Hemstock

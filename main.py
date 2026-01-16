from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from routers.routes import router
from sqlmodel import Session, select
from database import engine, init_words, create_db_and_tables
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # Create tables if they don't exist
        create_db_and_tables()
        print("Database tables created/verified")

        with Session(engine) as session:
            # Test database connection
            session.exec(select(1)).first()
        print("Database connected successfully!")
        await init_words()
    except Exception as e:
        print(f"FATAL: Database connection failed: {e}")
        raise

    yield
    print("Shutting down...")


# Initialize rate limiter from environment variable
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT])

app = FastAPI(
    title="Word Puzzle API",
    description="A Wordle-inspired word guessing game API",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "https://word-puzzle-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

app.include_router(router, prefix="/api")

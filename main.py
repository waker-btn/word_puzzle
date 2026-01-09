from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from routers.routes import router
from sqlmodel import Session, select
from database import engine, init_words
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
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

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

app.include_router(router)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.routes import router
from sqlmodel import Session, select
from database import engine, init_words


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
        print(f"Database connection failed: {e}")

    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(router)

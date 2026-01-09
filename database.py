from sqlmodel import Session, select, create_engine
from settings import settings
import requests
import random
from datetime import date, timedelta
from models.db import Words

database_url = f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PW}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(
    database_url,
    echo=settings.APP_ENV == "development",
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True,  # Verify connection is alive before using it
)


async def init_words():
    with Session(engine) as session:
        try:
            word_exists = session.exec(select(Words)).first()
            if not word_exists:
                print("Fetching initial word list...")
                response = requests.get(
                    "https://random-word-api.herokuapp.com/all",
                    timeout=10,
                )
                response.raise_for_status()

                values = response.json()
                if not values or not isinstance(values, list):
                    raise ValueError("Invalid response format from word API")

                valid_words = [
                    word for word in values if len(word) == 5 and word.isalpha()
                ]

                random.shuffle(valid_words)

                # Assign sequential dates starting from today
                start_date = date.today()

                for i, value in enumerate(valid_words):
                    word_date = start_date + timedelta(days=i)
                    word_entry = Words(word=value, date=word_date)
                    session.add(word_entry)
                session.commit()
                print(
                    f"Successfully loaded {len(valid_words)} words starting from {start_date}"
                )
        except requests.RequestException as e:
            print(f"Failed to fetch words from API: {e}")
            print("Consider pre-loading words manually")
        except Exception as e:
            print(f"Error initializing words: {e}")
            session.rollback()
            raise


def get_session():
    with Session(engine) as session:
        yield session

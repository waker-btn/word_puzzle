from sqlmodel import Session, select, create_engine
from settings import settings
import requests
from models.db import Words

database_url = f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PW}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(database_url, echo=settings.APP_ENV == "development")


async def init_words():
    with Session(engine) as session:
        word_exists = session.exec(select(Words)).first()
        if not word_exists:
            response = requests.get(
                "https://random-word-api.herokuapp.com/word?length=5&number=1000"
            )
            if response.status_code == 200:
                values = response.json()
                for value in values:
                    word_entry = Words(word=value)
                    session.add(word_entry)
                session.commit()

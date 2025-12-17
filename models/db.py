import uuid
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Enum as SQLEnum
from sqlmodel import ARRAY, Field, SQLModel, String


class GameStatus(str, Enum):
    ongoing = "ongoing"
    won = "won"
    lost = "lost"


class Words(SQLModel, table=True):
    word: str = Field(primary_key=True, max_length=5)


class Users(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    email: str = Field(max_length=100, unique=True)
    password: str = Field(max_length=100)


class Games(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    word: str = Field(foreign_key="words.word")
    attempts: Optional[list] = Field(
        default=None, sa_column=Column(ARRAY(String, dimensions=2))
    )
    remaining_attempts: int = Field(default=6)
    game_status: GameStatus = Field(
        default=GameStatus.ongoing, sa_column=Column(SQLEnum(GameStatus))
    )

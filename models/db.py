import uuid
from enum import Enum
from datetime import date as Date
from sqlalchemy import Column, Enum as SQLEnum, Date as SQLDate, UniqueConstraint
from sqlmodel import ARRAY, Field, SQLModel, String


class GameStatus(str, Enum):
    ongoing = "ongoing"
    won = "won"
    lost = "lost"


class Words(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    word: str = Field(max_length=5, index=True)
    date: Date = Field(sa_column=Column(SQLDate, unique=True, index=True))


class Users(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    username: str = Field(max_length=100, unique=True)
    password: str = Field(max_length=100)


class Games(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "date", name="unique_user_game_per_day"),
    )

    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    date: Date = Field(sa_column=Column(SQLDate, index=True))
    word: str = Field(max_length=5)  # Store the word directly, no foreign key needed
    attempts: list[list[str]] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String, dimensions=2)),
    )
    remaining_attempts: int = Field(default=6)
    game_status: GameStatus = Field(
        default=GameStatus.ongoing, sa_column=Column(SQLEnum(GameStatus))
    )

from sqlmodel import Column, Field, SQLModel
import sqlalchemy.dialects.postgresql as pg
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, sa_column=Column(pg.UUID, nullable=False, primary_key=True))
    username: str = Field(index=True, nullable=False, unique=True)
    password_hash: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
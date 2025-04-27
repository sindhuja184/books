from sqlmodel import SQLModel, Field, Column
from datetime import datetime, date
import sqlalchemy.dialects.postgresql as pg
import uuid

class Book(SQLModel, table=True):
    __tablename__ = 'books'

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default_factory=uuid.uuid4  # Automatically generates a UUID
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default_factory=datetime.utcnow)  # Automatically sets current UTC time
    )
    
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default_factory=datetime.utcnow)  # Automatically sets current UTC time
    )

    def __repr__(self):
        return f"<Book {self.title}>"

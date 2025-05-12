from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import datetime, date
import sqlalchemy.dialects.postgresql as pg
import uuid
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.auth.models import User
class Book(SQLModel, table = True):

    __tablename__ = "books"
    uid: uuid.UUID = Field(
        sa_column= Column(
            pg.UUID,
            nullable = False,
            primary_key= True,
            default = uuid.uuid4
        )
    )
    title: str
    author:  str
    publisher:  str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(
        default= None, 
        foreign_key= "users.uid")
    created_at:datetime = Field(
        sa_column = Column(pg.TIMESTAMP, default = datetime.now))
    updated_at: datetime = Field(sa_column = Column(pg.TIMESTAMP,  default = datetime.now))
    
    user: Optional["User"] = Relationship(
        back_populates="books"
    )

    def __repr__(self):
        return f"<Book {self.title}>"

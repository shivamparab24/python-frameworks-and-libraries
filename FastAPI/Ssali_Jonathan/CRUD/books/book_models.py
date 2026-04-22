import uuid

from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from FastAPI.Ssali_Jonathan.CRUD.core.database import Base


class Book(Base):
    __tablename__ = "books"

    uid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publisher = Column(String, nullable=False)
    published_date = Column(String)
    page_count = Column(Integer)
    language = Column(String)
    user_uid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uid"),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # user = relationship("User", back_populates="book", lazy="selectin")
    reviews = relationship("Review", back_populates="book", lazy = "selectin")

    tags = relationship("Tag", secondary = "book_tag", back_populates ="books", lazy = "selectin")

    def __repr__(self):
        return f"<Book {self.title}>"
    
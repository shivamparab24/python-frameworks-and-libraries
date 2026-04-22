import uuid

from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from FastAPI.Ssali_Jonathan.CRUD.core.database import Base


class Review(Base):
    __tablename__ = "reviews"

    uid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    rating = Column(Integer)
    review = Column(String)

    user_uid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uid"),
        nullable=True
    )

    book_uid = Column(
        UUID(as_uuid=True),
        ForeignKey("books.uid"),
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

    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")

    # book = relationship("Book", back_populates="reviews", lazy="selectin")

    def __repr__(self):
        return f"<Review for book {self.book_uid} by User {self.user_uid}>"
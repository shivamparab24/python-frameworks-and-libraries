from datetime import datetime
import uuid

from sqlalchemy import Column, ForeignKey, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from FastAPI.Ssali_Jonathan.CRUD.core.database import Base



class Tag(Base):
    __tablename__ = "tags"

    uid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    name = Column(String, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


    books = relationship("Book", secondary = "book_tag", back_populates = "tags", lazy = "selectin")

    def __repr__(self):
        return f"<Tag {self.name}>"
    



class BookTag(Base):
    __tablename__ = "book_tag"

    book_id = Column(UUID(as_uuid=True), ForeignKey("books.uid"), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.uid"), primary_key=True)
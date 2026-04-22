import uuid

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from FastAPI.Ssali_Jonathan.CRUD.core.database import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    username = Column(String(100), nullable=False, unique=True, index=True)
    email = Column(String, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    password_hash = Column(String(100), nullable=False)
    role = Column(String, nullable=False, server_default="user")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False
    )

    # book = relationship("Book", back_populates="user", lazy="selectin")

    reviews = relationship("Review", back_populates="user") 
    
    def __repr__(self):
        return f"<User(username={self.username})>"
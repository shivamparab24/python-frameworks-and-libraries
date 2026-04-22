from pydantic import BaseModel, ConfigDict, Field
import uuid
from datetime import datetime
from typing import List, Optional

from FastAPI.Ssali_Jonathan.CRUD.reviews.review_schema import ReviewModel
from FastAPI.Ssali_Jonathan.CRUD.tags.tags_schema import TagCreateModel


class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime
    # user: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class CreateBook(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    published_date: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None

class BookDetails(Book):
    reviews: List[ReviewModel]
    tags: List[TagCreateModel]
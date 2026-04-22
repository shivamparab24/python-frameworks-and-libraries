from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import List, Optional

from FastAPI.Ssali_Jonathan.CRUD.books.book_schema import Book, CreateBook
from FastAPI.Ssali_Jonathan.CRUD.reviews.review_schema import ReviewModel


class UserResponse(BaseModel):
    uid: uuid.UUID
    username: Optional[str] = None
    email: str
    first_name: str
    last_name: str
    password_hash: str = Field(exclude=True)
    is_verified: bool
    role: str = Field()
    created_at: datetime
    updated_at: datetime


class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    first_name: Optional[str]
    last_name: Optional[str]


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

class UserBooksModel(UserResponse):
    books: Optional[List[Book]] = []
    reviews: Optional[list[ReviewModel]] = []


class EmailModel(BaseModel):
    email_addr: List[str]


class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str
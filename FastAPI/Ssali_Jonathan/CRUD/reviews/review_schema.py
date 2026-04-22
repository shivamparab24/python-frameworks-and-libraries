from pydantic import BaseModel, ConfigDict, Field
import uuid
from datetime import datetime
from typing import Optional


class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(lt=5)
    review: str
    user_uid: Optional[uuid.UUID] = None
    book_uid: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime   

    model_config = ConfigDict(from_attributes=True)


class ReviewCreateModel(BaseModel):
    rating: int = Field(ge=1, le=5)
    review: str 


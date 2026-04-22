from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession

from FastAPI.Ssali_Jonathan.CRUD.auth.user_models import User
from FastAPI.Ssali_Jonathan.CRUD.core.database import get_session
from FastAPI.Ssali_Jonathan.CRUD.reviews.review_schema import ReviewCreateModel, ReviewModel
from FastAPI.Ssali_Jonathan.CRUD.reviews.review_service import ReviewService
from FastAPI.Ssali_Jonathan.CRUD.utils.dependencies import RoleChecker, get_current_user

review_router = APIRouter()
review_service = ReviewService()
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["user", "admin"]))

@review_router.post('/book/{book_uid}', response_model=ReviewModel, dependencies=[user_role_checker])
async def add_review_to_books(
    book_uid: str,
    review: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    new_review = await review_service.add_review_to_book(
        user_email = current_user.email,
        review = review,
        book_uid = book_uid,
        session = session
    )

    return new_review


@review_router.get("/", response_model=ReviewModel, dependencies=[admin_role_checker])
async def get_all_reviews(session: AsyncSession = Depends(get_session)):
    review = await review_service.get_all_reviews(session)

    return review


@review_router.get("/{uid}", response_model=ReviewModel, dependencies=[user_role_checker])
async def get_review(uid: str, session: AsyncSession = Depends(get_session)):
    review = await review_service.get_review(uid, session)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    return review


@review_router.delete("/{uid}", dependencies=[user_role_checker], status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    uid: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await review_service.delete_review_from_book(
        uid = uid, user_email = current_user.email, session = session
    )

    return None
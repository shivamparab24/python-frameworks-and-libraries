import logging

from sqlalchemy import desc, select

from FastAPI.Ssali_Jonathan.CRUD.auth.user_service import UserService
from FastAPI.Ssali_Jonathan.CRUD.books.book_service import BookService
from FastAPI.Ssali_Jonathan.CRUD.reviews.review_models import Review
from FastAPI.Ssali_Jonathan.CRUD.reviews.review_schema import ReviewCreateModel, ReviewModel

from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio.session import AsyncSession

book_service = BookService()
user_service = UserService()

class ReviewService:

    async def add_review_to_book(
        self,
        user_email: str, 
        book_uid: str,   
        review: ReviewCreateModel, 
        session: AsyncSession
    ):
        try:
            book = await book_service.get_book(
                book_uid = book_uid,
                session = session
            )

            user = await user_service.get_user_by_email(
                email = user_email,
                session = session
            )

            review_data_dict = review.model_dump()

            new_review = Review(
                **review_data_dict
            )

            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail = "Book Not Found"
                )
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail = "User Not Found"
                )

            new_review.user = user
            new_review.book = book

            session.add(new_review)

            await session.commit()

            return new_review
        
        except HTTPException:
            raise
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Oops... Something Went Wrong'
            )
        

    async def get_review(self, review_uid: str, session: AsyncSession):
        statement = select(Review).where(Review.uid == review_uid)
        result = await session.scalars(statement)
        return result.first()


    async def get_all_reviews(self, session: AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))
        result = await session.scalars(statement)
        return result.all()


    async def delete_review_from_book(
        self, review_uid: str, user_email: str, session: AsyncSession
    ):
        user = await user_service.get_user_by_email(user_email, session)

        review = await self.get_review(review_uid, session)

        if not review or (review.user != user):
            raise HTTPException(
                detail="Cannot delete this review",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        session.delete(review)

        await session.commit()
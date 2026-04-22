import uuid
from alembic.util import status
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from FastAPI.Ssali_Jonathan.CRUD.books.book_models import Book
from FastAPI.Ssali_Jonathan.CRUD.books.book_schema import CreateBook, UpdateBook


class BookService:

    async def get_all_books(self, session: AsyncSession):
        stmt = (
            select(Book)
            # .options(selectinload(Book.reviews))
            .order_by(desc(Book.created_at))
        )
        result = await session.execute(stmt)
        return result.scalars().all()


    async def get_user_books(self, user_uid: str, session: AsyncSession):
        stmt = (
            select(Book)
            # .options(selectinload(Book.reviews))
            .where(Book.user_uid == user_uid)
            .order_by(desc(Book.created_at))
        )
        result = await session.execute(stmt)
        return result.scalars().all()


    async def get_book(self, book_uid: uuid.UUID, session: AsyncSession):
        stmt = (
            select(Book)
            # .options(selectinload(Book.reviews))
            .where(Book.uid == book_uid)
        )
        result = await session.execute(stmt)
        return result.scalars().first()


    async def create_book(self, book_data: CreateBook, user_uid: str, session: AsyncSession):
        book_data_dict = book_data.model_dump()

        new_book = Book(
            **book_data_dict
        )
        new_book.published_date = book_data_dict['published_date']

        new_book.user_uid = uuid.UUID(user_uid)

        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)

        return new_book


    async def update_book(self, book_uid: uuid.UUID, update_data: UpdateBook, session: AsyncSession):
        updated_book = await self.get_book(book_uid, session)

        if not updated_book: 
            return None

        for k, v in update_data.model_dump(exclude_unset=True).items():
            setattr(updated_book, k, v)

        async with session.begin():
            pass  # changes auto-tracked

        await session.refresh(updated_book)

        return updated_book


    async def delete_book(self, book_uid: uuid.UUID, session: AsyncSession):
        book = await self.get_book(book_uid, session)

        if book is None:
            return None

        await session.delete(book)
        await session.commit()

        return book
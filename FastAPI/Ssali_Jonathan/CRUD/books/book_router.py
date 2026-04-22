import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession

from FastAPI.Ssali_Jonathan.CRUD.core.database import get_session
from FastAPI.Ssali_Jonathan.CRUD.books.book_service import BookService
from FastAPI.Ssali_Jonathan.CRUD.books.book_schema import (
    Book,
    CreateBook,
    UpdateBook,
    BookDetails
)
from FastAPI.Ssali_Jonathan.CRUD.core.errors import BookNotFound
from FastAPI.Ssali_Jonathan.CRUD.utils.dependencies import AccessTokenBearer, RoleChecker


book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(['admin', 'user']))


@book_router.get("/", response_model=List[BookDetails], dependencies = [role_checker])
async def get_all_the_books(
    session: AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
):

    # print(token_details)
    return await book_service.get_all_books(session)


@book_router.get("/user/{user_uid}", response_model=List[BookDetails], dependencies = [role_checker])
async def get_user_book_submissions(
    user_uid: str,
    session: AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
):
    # print(token_details)
    return await book_service.get_user_books(user_uid, session)



@book_router.post(
    "/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    dependencies = [role_checker]
)
async def create_a_book(
    book_data: CreateBook,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
) -> dict:
    
    print("Token Details: ")
    print(token_details)
    print()
    user_id = token_details.get("user")["user_uuid"]

    return await book_service.create_book(book_data, user_id, session)


@book_router.get(
        "/{book_uid}",
        response_model = BookDetails,
        dependencies = [role_checker]
)
async def get_a_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    book = await book_service.get_book(book_uid, session)

    if not book:
        # raise HTTPException(
        #     status_code=status.HTTP_404_NOT_FOUND,
        #     detail="Book not found"
        # )
        raise BookNotFound()
    
    return book


@book_router.patch("/{book_uid}", response_model=BookDetails, dependencies = [role_checker])
async def update_a_book(
    book_uid: uuid.UUID,
    up_book: UpdateBook,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    updated_book = await book_service.update_book(book_uid, up_book, session)

    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    return updated_book


@book_router.delete(
    "/{book_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies = [role_checker]
)
async def delete_a_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    deleted = await book_service.delete_book(book_uid, session)

    if deleted is None:
        # raise HTTPException(
        #     status_code=status.HTTP_404_NOT_FOUND,
        #     detail="Book not found"
        # )
        raise BookNotFound()
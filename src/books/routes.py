from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.data import data
from src.books.schemas import Book, BookUpdateModel, BookCreateModel, BoookDetailModel
from src.books.service import BookService
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.errors import *

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_service = RoleChecker(["admin", "user"])


@book_router.get("/", response_model=List[Book])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    _: bool = Depends(role_service),
):
    book = await book_service.get_all_books(session)
    return book


@book_router.get("/user/{user_uid}", response_model=List[Book])
async def get_user_books(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    _: bool = Depends(role_service),
):
    book = await book_service.get_user_books(user_uid, session)
    return book


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    _: bool = Depends(role_service),
):
    print(token_details)
    user_id = token_details.get("user")["user_id"]  # type:ignore
    new_book = await book_service.create_book(
        book_data, user_id, session
    )  # type:ignore
    return new_book  # type:ignore


@book_router.get("/{book_id}", response_model=BoookDetailModel)
async def get_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    _: bool = Depends(role_service),
):
    book = await book_service.get_books(str(book_id), session)
    if book:
        return book
    else:
        raise UnableToFetchResource()


@book_router.patch("/{book_id}")
async def update_book(
    book_id: str,
    update_info: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    _: bool = Depends(role_service),
):

    updatedBook = await book_service.update_book(str(book_id), update_info, session)
    if updatedBook:
        return updatedBook
    else:
        raise UnableToFetchResource()


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    _: bool = Depends(role_service),
):
    getrid = await book_service.delete_book(str(book_id), session)
    if getrid is None:
        raise UnableToFetchResource()
    else:
        return None

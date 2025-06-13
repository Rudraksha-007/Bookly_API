from src.db.models import Reviews
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel
from fastapi import status
from src.errors import *
import logging

# from pydantic import mode
book_service = BookService()
user_service = UserService()


class ReviewService:

    async def add_review_to_book(
        self,
        user_email: str,
        book_id: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        try:
            book = await book_service.get_books(book_id, session)  # type:ignore
            if not book:
                raise UnableToFetchResource()
            user = await user_service.get_user_by_email(user_email, session)
            if not user:
                raise UnableToFetchResource()

            data_dict = review_data.model_dump()
            new_review = Reviews(**data_dict)  # type:ignore
            # print(new_review)
            new_review.user = user
            new_review.book = book

            session.add(new_review)
            await session.commit()
            return new_review

        except Exception as error:
            logging.exception(error)
            raise InternalServerError()

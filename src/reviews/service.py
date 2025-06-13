from src.db.models import Reviews
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel
from fastapi.exceptions import HTTPException
from fastapi import status
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
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="The Book requested could'nt be located"
                )
            user = await user_service.get_user_by_email(user_email, session)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="The User requested could'nt be located",
                )
            
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
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oops... Something went wrong :-C",
            )
        

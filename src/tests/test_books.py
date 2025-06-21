book_prefix = f"/api/v1/books"


def test_get_allBooks(test_client, fake_book_service, fake_session):
    response = test_client.get(
        url=f"{book_prefix}",
    )

    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)

def test_get_user_books(test_client,fake_book_service,fake_session):
    user_id=213421
    response=test_client.get(
        url=f"{book_prefix}/user/{user_id}",
    )

    assert fake_book_service.get_user_books_called_once()
    assert fake_book_service.get_user_books_called_once_with(fake_session)

def test_create_book(test_client,fake_book_service,fake_session):
    response=test_client.post(url="/")

    assert fake_book_service.create_book_called_once()
    assert fake_book_service.create_book_called_once_with(fake_session)


def test_get_book(test_client,fake_session,fake_book_service):
    book_id=2345680
    response=test_client.get(url=f"{book_prefix}/{book_id}")

    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(fake_session)

def test_update_book(test_client,fake_session,fake_book_service):
    book_id=2345680
    response=test_client.patch(url=f"{book_prefix}/{book_id}")

    assert fake_book_service.update_book_called_once()
    assert fake_book_service.update_book_called_once_with(fake_session)

def test_delete_book(test_client,fake_session,fake_book_service):
    book_id=2345680
    response=test_client.delete(url=f"{book_prefix}/{book_id}")

    assert fake_book_service.delete_book_called_once()
    assert fake_book_service.delete_book_called_once_with(fake_session)

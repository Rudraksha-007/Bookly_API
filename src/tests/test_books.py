book_prefix = f"/api/v1/books"


def test_get_allBooks(test_client, fake_book_service, fake_session):
    response = test_client.get(
        url=f"{book_prefix}",
    )

    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)


def test_get_user_books(test_client, fake_book_service, fake_session):
    user_id = 213421
    response = test_client.get(
        url=f"{book_prefix}/user/{user_id}",
    )

    assert fake_book_service.get_user_books_called_once()
    assert fake_book_service.get_user_books_called_once_with(fake_session)


def test_create_book(test_client, fake_book_service, fake_session):
    response = test_client.post(url="/")

    assert fake_book_service.create_book_called_once()
    assert fake_book_service.create_book_called_once_with(fake_session)


def test_get_book(test_client, fake_session, fake_book_service):
    book_id = 2345680
    response = test_client.get(url=f"{book_prefix}/{book_id}")

    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(fake_session)


def test_update_book(test_client, fake_session, fake_book_service):
    book_id = 2345680
    response = test_client.patch(url=f"{book_prefix}/{book_id}")

    assert fake_book_service.update_book_called_once()
    assert fake_book_service.update_book_called_once_with(fake_session)


def test_delete_book(test_client, fake_session, fake_book_service):
    book_id = 2345680
    response = test_client.delete(url=f"{book_prefix}/{book_id}")

    assert fake_book_service.delete_book_called_once()
    assert fake_book_service.delete_book_called_once_with(fake_session)


def test_get_allBooks_empty(test_client, fake_book_service, fake_session):
    fake_book_service.get_all_books.return_value = []
    response = test_client.get(url=f"{book_prefix}")
    assert response.status_code == 200
    assert response.json() == []
    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)


def test_get_allBooks_error(test_client, fake_book_service, fake_session):
    fake_book_service.get_all_books.side_effect = Exception("DB error")
    response = test_client.get(url=f"{book_prefix}")
    assert response.status_code == 500
    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)


def test_get_user_books_empty(test_client, fake_book_service, fake_session):
    user_id = 1
    fake_book_service.get_user_books.return_value = []
    response = test_client.get(url=f"{book_prefix}/user/{user_id}")
    assert response.status_code == 200
    assert response.json() == []
    assert fake_book_service.get_user_books_called_once()
    assert fake_book_service.get_user_books_called_once_with(fake_session)


def test_get_user_books_not_found(test_client, fake_book_service, fake_session):
    user_id = 9999
    fake_book_service.get_user_books.return_value = None
    response = test_client.get(url=f"{book_prefix}/user/{user_id}")
    assert response.status_code == 404
    assert fake_book_service.get_user_books_called_once()
    assert fake_book_service.get_user_books_called_once_with(fake_session)


def test_create_book_invalid_payload(test_client, fake_book_service, fake_session):
    response = test_client.post(url="/", json={"invalid": "data"})
    assert response.status_code == 422
    assert not fake_book_service.create_book_called_once()


def test_create_book_duplicate(test_client, fake_book_service, fake_session):
    fake_book_service.create_book.side_effect = Exception("Duplicate")
    response = test_client.post(url="/")
    assert response.status_code == 400
    assert fake_book_service.create_book_called_once()
    assert fake_book_service.create_book_called_once_with(fake_session)


def test_get_book_not_found(test_client, fake_session, fake_book_service):
    book_id = 9999
    fake_book_service.get_book.return_value = None
    response = test_client.get(url=f"{book_prefix}/{book_id}")
    assert response.status_code == 404
    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(fake_session)


def test_update_book_not_found(test_client, fake_session, fake_book_service):
    book_id = 9999
    fake_book_service.update_book.return_value = None
    response = test_client.patch(url=f"{book_prefix}/{book_id}")
    assert response.status_code == 404
    assert fake_book_service.update_book_called_once()
    assert fake_book_service.update_book_called_once_with(fake_session)


def test_update_book_invalid_payload(test_client, fake_session, fake_book_service):
    book_id = 2345680
    response = test_client.patch(url=f"{book_prefix}/{book_id}", json={"bad": "data"})
    assert response.status_code == 422
    assert not fake_book_service.update_book_called_once()


def test_delete_book_not_found(test_client, fake_session, fake_book_service):
    book_id = 9999
    fake_book_service.delete_book.return_value = None
    response = test_client.delete(url=f"{book_prefix}/{book_id}")
    assert response.status_code == 404
    assert fake_book_service.delete_book_called_once()
    assert fake_book_service.delete_book_called_once_with(fake_session)


def test_delete_book_unauthorized(test_client, fake_session, fake_book_service):
    book_id = 2345680
    response = test_client.delete(url=f"{book_prefix}/{book_id}", headers={"Authorization": "Invalid"})
    assert response.status_code == 401
    assert not fake_book_service.delete_book_called_once()


def test_get_allBooks_large(test_client, fake_book_service, fake_session):
    fake_book_service.get_all_books.return_value = [{}] * 1000
    response = test_client.get(url=f"{book_prefix}")
    assert response.status_code == 200
    assert len(response.json()) == 1000
    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)


def test_create_book_missing_fields(test_client, fake_book_service, fake_session):
    response = test_client.post(url="/", json={})
    assert response.status_code == 422
    assert not fake_book_service.create_book_called_once()


def test_update_book_no_changes(test_client, fake_session, fake_book_service):
    book_id = 2345680
    fake_book_service.update_book.return_value = {}
    response = test_client.patch(url=f"{book_prefix}/{book_id}", json={})
    assert response.status_code == 200
    assert fake_book_service.update_book_called_once()
    assert fake_book_service.update_book_called_once_with(fake_session)


def test_delete_book_already_deleted(test_client, fake_session, fake_book_service):
    book_id = 2345680
    fake_book_service.delete_book.side_effect = Exception("Already deleted")
    response = test_client.delete(url=f"{book_prefix}/{book_id}")
    assert response.status_code == 400
    assert fake_book_service.delete_book_called_once()
    assert fake_book_service.delete_book_called_once_with(fake_session)


def test_get_book_invalid_id(test_client, fake_session, fake_book_service):
    book_id = "invalid"
    response = test_client.get(url=f"{book_prefix}/{book_id}")
    assert response.status_code == 422
    assert not fake_book_service.get_book_called_once()


def test_update_book_invalid_id(test_client, fake_session, fake_book_service):
    book_id = "invalid"
    response = test_client.patch(url=f"{book_prefix}/{book_id}")
    assert response.status_code == 422
    assert not fake_book_service.update_book_called_once()


def test_delete_book_invalid_id(test_client, fake_session, fake_book_service):
    book_id = "invalid"
    response = test_client.delete(url=f"{book_prefix}/{book_id}")
    assert response.status_code == 422
    assert not fake_book_service.delete_book_called_once()


def test_create_book_large_payload(test_client, fake_book_service, fake_session):
    large_data = {"title": "A" * 10000}
    response = test_client.post(url="/", json=large_data)
    assert response.status_code in (201, 400, 413)


def test_update_book_large_payload(test_client, fake_session, fake_book_service):
    book_id = 2345680
    large_data = {"title": "A" * 10000}
    response = test_client.patch(url=f"{book_prefix}/{book_id}", json=large_data)
    assert response.status_code in (200, 400, 413)


def test_create_book_unauthorized(test_client, fake_book_service, fake_session):
    response = test_client.post(url="/", headers={"Authorization": "Invalid"})
    assert response.status_code == 401
    assert not fake_book_service.create_book_called_once()


def test_update_book_unauthorized(test_client, fake_session, fake_book_service):
    book_id = 2345680
    response = test_client.patch(url=f"{book_prefix}/{book_id}", headers={"Authorization": "Invalid"})
    assert response.status_code == 401
    assert not fake_book_service.update_book_called_once()


def test_get_allBooks_unauthorized(test_client, fake_book_service, fake_session):
    response = test_client.get(url=f"{book_prefix}", headers={"Authorization": "Invalid"})
    assert response.status_code == 401
    assert not fake_book_service.get_all_books_called_once()


def test_get_user_books_unauthorized(test_client, fake_book_service, fake_session):
    user_id = 1
    response = test_client.get(url=f"{book_prefix}/user/{user_id}", headers={"Authorization": "Invalid"})
    assert response.status_code == 401
    assert not fake_book_service.get_user_books_called_once()


def test_get_book_unauthorized(test_client, fake_session, fake_book_service):
    book_id = 2345680
    response = test_client.get(url=f"{book_prefix}/{book_id}", headers={"Authorization": "Invalid"})
    assert response.status_code == 401
    assert not fake_book_service.get_book_called_once()


def test_update_book_forbidden(test_client, fake_session, fake_book_service):
    book_id = 2345680
    response = test_client.patch(url=f"{book_prefix}/{book_id}", headers={"Authorization": "Forbidden"})
    assert response.status_code == 403
    assert not fake_book_service.update_book_called_once()


def test_delete_book_forbidden(test_client, fake_session, fake_book_service):
    book_id = 2345680
    response = test_client.delete(url=f"{book_prefix}/{book_id}", headers={"Authorization": "Forbidden"})
    assert response.status_code == 403
    assert not fake_book_service.delete_book_called_once()


def test_create_book_forbidden(test_client, fake_book_service, fake_session):
    response = test_client.post(url="/", headers={"Authorization": "Forbidden"})
    assert response.status_code == 403
    assert not fake_book_service.create_book_called_once()


def test_get_allBooks_forbidden(test_client, fake_book_service, fake_session):
    response = test_client.get(url=f"{book_prefix}", headers={"Authorization": "Forbidden"})
    assert response.status_code == 403
    assert not fake_book_service.get_all_books_called_once()


def test_get_user_books_forbidden(test_client, fake_book_service, fake_session):
    user_id = 1
    response = test_client.get(url=f"{book_prefix}/user/{user_id}", headers={"Authorization": "Forbidden"})
    assert response.status_code == 403
    assert not fake_book_service.get_user_books_called_once()


def test_get_book_forbidden(test_client, fake_session, fake_book_service):
    book_id = 2345680
    response = test_client.get(url=f"{book_prefix}/{book_id}", headers={"Authorization": "Forbidden"})
    assert response.status_code == 403
    assert not fake_book_service.get_book_called_once()


def test_create_book_no_auth_header(test_client, fake_book_service, fake_session):
    response = test_client.post(url="/")
    assert response.status_code in (201, 401)


def test_update_book_no_auth_header(test_client, fake_session, fake_book_service):
    book_id = 2345680
    response = test_client.patch(url=f"{book_prefix}/{book_id}")
    assert response.status_code in (200, 401)


def test_delete_book_no_auth_header(test_client, fake_session, fake_book_service):
    book_id = 2345680
    response = test_client.delete(url=f"{book_prefix}/{book_id}")
    assert response.status_code in (200, 401)


def test_get_allBooks_no_auth_header(test_client, fake_book_service, fake_session):
    response = test_client.get(url=f"{book_prefix}")
    assert response.status_code in (200, 401)


def test_get_user_books_no_auth_header(test_client, fake_book_service, fake_session):
    user_id = 1
    response = test_client.get(url=f"{book_prefix}/user/{user_id}")
    assert response.status_code in (200, 401)


def test_get_book_no_auth_header(test_client, fake_session, fake_book_service):
    book_id = 2345680
    response = test_client.get(url=f"{book_prefix}/{book_id}")
    assert response.status_code in (200, 401)


def test_create_book_db_down(test_client, fake_book_service, fake_session):
    fake_book_service.create_book.side_effect = Exception("DB down")
    response = test_client.post(url="/")
    assert response.status_code == 500
    assert fake_book_service.create_book_called_once()
    assert fake_book_service.create_book_called_once_with(fake_session)


def test_update_book_db_down(test_client, fake_session, fake_book_service):
    book_id = 2345680
    fake_book_service.update_book.side_effect = Exception("DB down")
    response = test_client.patch(url=f"{book_prefix}/{book_id}")
    assert response.status_code == 500
    assert fake_book_service.update_book_called_once()
    assert fake_book_service.update_book_called_once_with(fake_session)


def test_delete_book_db_down(test_client, fake_session, fake_book_service):
    book_id = 2345680
    fake_book_service.delete_book.side_effect = Exception("DB down")
    response = test_client.delete(url=f"{book_prefix}/{book_id}")
    assert response.status_code == 500
    assert fake_book_service.delete_book_called_once()
    assert fake_book_service.delete_book_called_once_with(fake_session)


def test_get_allBooks_db_down(test_client, fake_book_service, fake_session):
    fake_book_service.get_all_books.side_effect = Exception("DB down")
    response = test_client.get(url=f"{book_prefix}")
    assert response.status_code == 500
    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)


def test_get_user_books_db_down(test_client, fake_book_service, fake_session):
    user_id = 1
    fake_book_service.get_user_books.side_effect = Exception("DB down")
    response = test_client.get(url=f"{book_prefix}/user/{user_id}")
    assert response.status_code == 500
    assert fake_book_service.get_user_books_called_once()
    assert fake_book_service.get_user_books_called_once_with(fake_session)


def test_get_book_db_down(test_client, fake_session, fake_book_service):
    book_id = 2345680
    fake_book_service.get_book.side_effect = Exception("DB down")
    response = test_client.get(url=f"{book_prefix}/{book_id}")
    assert response.status_code == 500
    assert fake_book_service.get_book_called_once()
    assert fake_book_service.get_book_called_once_with(fake_session)


def test_create_book_bulk(test_client, fake_book_service, fake_session):
    for _ in range(10):
        response = test_client.post(url="/")
        assert response.status_code in (201, 400)
    assert fake_book_service.create_book.call_count == 10


def test_update_book_bulk(test_client, fake_session, fake_book_service):
    book_id = 2345680
    for _ in range(10):
        response = test_client.patch(url=f"{book_prefix}/{book_id}")
        assert response.status_code in (200, 400)
    assert fake_book_service.update_book.call_count == 10


def test_delete_book_bulk(test_client, fake_session, fake_book_service):
    book_id = 2345680
    for _ in range(10):
        response = test_client.delete(url=f"{book_prefix}/{book_id}")
        assert response.status_code in (200, 400)
    assert fake_book_service.delete_book.call_count == 10


def test_get_allBooks_bulk(test_client, fake_book_service, fake_session):
    for _ in range(10):
        response = test_client.get(url=f"{book_prefix}")
        assert response.status_code == 200
    assert fake_book_service.get_all_books.call_count == 10


def test_get_user_books_bulk(test_client, fake_book_service, fake_session):
    user_id = 1
    for _ in range(10):
        response = test_client.get(url=f"{book_prefix}/user/{user_id}")
        assert response.status_code == 200
    assert fake_book_service.get_user_books.call_count == 10


def test_get_book_bulk(test_client, fake_session, fake_book_service):
    book_id = 2345680
    for _ in range(10):
        response = test_client.get(url=f"{book_prefix}/{book_id}")
        assert response.status_code == 200
    assert fake_book_service.get_book.call_count == 10

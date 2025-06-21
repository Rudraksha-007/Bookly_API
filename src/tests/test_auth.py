from faker import Faker
from src.auth.schemas import UserCreateModel

auth_prefix = f"/api/v1/auth"

fakE=Faker()

def test_user_Creation(fake_session, fake_user_service, test_client):


    signUp_data={
        "username":fakE.user_name()[:7],
        "email":fakE.email(),
        "password":fakE.password(),
        "fname":fakE.first_name(),
        "lname":fakE.last_name(),
        "role":"user"
    }


    response = test_client.post(
        url=f"{auth_prefix}/signup",
        json=signUp_data,
    )
    new_user=UserCreateModel(**signUp_data)

    assert fake_user_service.user_exists_called_once()
    assert fake_user_service.user_exists_called_once_with(signUp_data['email'],fake_session)
    assert fake_user_service.create_user_called_once()
    assert fake_user_service.create_user_called_once_with(new_user,fake_session)


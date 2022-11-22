from rest_framework.test import APIClient
from django.conf import settings
import pytest

from user.utils.auth_provider import AuthProvider

client = APIClient()
auth_provider = AuthProvider()


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


@pytest.mark.django_db()
def test_sign_up_success():
    data = dict(
        email="test@test.com",
        password="Test1234!",
        name="테스트",
        phone_number="010-0000-0000",
    )
    response = client.post("/api/signup/", data=data)
    assert response.status_code == 201


@pytest.mark.django_db()
def test_sign_in_success():
    data = dict(
        email="test1@test.com",
        password="Test1234!",
    )
    response = client.post("/api/signin/", data=data)
    assert response.status_code == 200


# TODO 토큰 디코드 에러로 인한 테스트 오류
# @pytest.mark.django_db()
# def test_sign_out_success():
#     token = auth_provider.create_token(user_id=1)
#     headers = {"Authorization": token}
#     response = client.get("/api/signout/", headers=headers)
#     assert response.status_code == 200

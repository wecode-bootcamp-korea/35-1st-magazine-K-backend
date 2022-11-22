from rest_framework.test import APIClient
from django.conf import settings
import pytest

from user.utils.auth_provider import AuthProvider

client = APIClient()

auth_provider = AuthProvider()


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


"""
리뷰 CRUD 테스트
"""


# @pytest.mark.django_db()
# def test_create_review_success():
#     token = auth_provider.create_token(user_id=1)
#     headers = {"Authorization": token}
#     data = {"content": "테스트 리뷰", "rating": 5}
#     response = client.post("/api/product/2/review/", data=data, headers=headers)
#     assert response.status_code == 201


@pytest.mark.django_db()
def test_get_review_list_success():
    response = client.get("/api/product/2/review/")
    assert response.status_code == 200


# @pytest.mark.django_db()
# def test_update_cart_item_success():
#     token = auth_provider.create_token(user_id=1)
#     headers = {"Authorization": token}
#     response = client.put("/api/product/review/<int:review_id>/", headers=headers)
#     assert response.status_code == 200


# @pytest.mark.django_db()
# def test_delete_cart_item_success():
#     token = auth_provider.create_token(user_id=1)
#     headers = {"Authorization": token}
#     response = client.delete("/api/product/review/<int:review_id>/", headers=headers)
#     assert response.status_code == 200

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
장바구니 CRUD 테스트
"""


# @pytest.mark.django_db()
# def test_create_cart_item_success():
#     token = auth_provider.create_token(user_id=1)
#     headers = {"Authorization": token}
#     payload = {"product_id": 5, "order_quantity": 1}
#     response = client.post("/api/cart/", payload, headers=headers)
#     assert response.status_code == 201


# @pytest.mark.django_db()
# def test_get_cart_item_list_success():
#     token = auth_provider.create_token(user_id=1)
#     headers = {"Authorization": token}
#     response = client.get("/api/cart/", headers=headers)
#     assert response.status_code == 200


# @pytest.mark.django_db()
# def test_update_cart_item_success():
#     token = auth_provider.create_token(user_id=1)
#     headers = {"Authorization": token}
#     response = client.put("/api/cart/1/1/", headers=headers)
#     assert response.status_code == 200


# @pytest.mark.django_db()
# def test_delete_cart_item_success():
#     token = auth_provider.create_token(user_id=1)
#     headers = {"Authorization": token}
#     response = client.delete("/api/cart/1/", headers=headers)
#     assert response.status_code == 200

"""
주문 관련 테스트
"""


# @pytest.mark.django_db()
# def test_order_item_success():
#     token = auth_provider.create_token(user_id=1)
#     headers = {"Authorization": token}
#     response = client.put("/api/order/", headers=headers)
#     assert response.status_code == 200


"""
주문 상태 CRUD 테스트
"""


@pytest.mark.django_db()
def test_create_order_status_success():
    data = {"order_status": "test"}
    response = client.post("/api/order/status/", data=data)
    assert response.status_code == 201

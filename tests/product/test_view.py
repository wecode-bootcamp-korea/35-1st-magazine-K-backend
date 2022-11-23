from rest_framework.test import APIClient
from django.conf import settings
import pytest

client = APIClient()


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


"""
카테고리 CRUD 테스트
"""


@pytest.mark.django_db()
def test_create_category_success():
    data = {"name": "테스트"}
    response = client.post("/api/category/", data=data)
    assert response.status_code == 201


@pytest.mark.django_db()
def test_get_category_list_success():
    response = client.get("/api/category/")
    assert response.status_code == 200


@pytest.mark.django_db()
def test_update_category_success():
    data = {"name": "테스트"}
    response = client.put("/api/category/1/", data=data)
    assert response.status_code == 200


@pytest.mark.django_db()
def test_delete_category_success():
    response = client.delete("/api/category/1/")
    assert response.status_code == 200


"""
상품 CRRUD 테스트
"""


@pytest.mark.django_db()
def test_create_product_success():
    data = {
        "title": "테스트",
        "price": 10000,
        "language": "ko",
        "size": "테스트 x 테스트 mm",
        "pages": 100,
        "published_date": "20xx. xx. xx",
        "isbn": "xxx-xx-xxxx-xxx-x",
        "description": "테스트",
        "issue_number": 1,
        "product_image_url": "테스트",
        "main_category": 1,
        "sub_category": 2,
        "main_url": "테스트",
        "sub_url": "테스트",
    }
    response = client.post("/api/product/", data=data)
    assert response.status_code == 201


@pytest.mark.django_db()
def test_get_product_detail_success():
    response = client.get("/api/product/5/")
    assert response.status_code == 200


@pytest.mark.django_db()
def test_get_product_list_success():
    response = client.get("/api/product/list/")
    assert response.status_code == 200


@pytest.mark.django_db()
def test_update_product_success():
    data = {
        "title": "테스트",
        "price": 10000,
        "language": "ko",
        "size": "테스트 x 테스트 mm",
        "pages": 100,
        "published_date": "20xx. xx. xx",
        "isbn": "xxx-xx-xxxx-xxx-x",
        "description": "테스트",
        "issue_number": 1,
        "product_image_url": "테스트",
        "main_category": 1,
        "sub_category": 2,
        "main_url": "테스트",
        "sub_url": "테스트",
    }
    response = client.put("/api/product/5/", data=data)
    assert response.status_code == 200


@pytest.mark.django_db()
def test_delete_product_success():
    response = client.delete("/api/product/2/")
    assert response.status_code == 200

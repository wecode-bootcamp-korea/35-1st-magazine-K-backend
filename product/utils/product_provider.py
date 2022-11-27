from typing import List

from django.db import transaction

from ..serializers import ProductRepo, ProductImageRepo
from core.exceptions import DuplicateError


class ProductService:
    """
    상품 CRRUD 관련 서비스 로직 제공 클래스
    """

    def __init__(self) -> None:
        self.product_repo = ProductRepo()
        self.product_image_repo = ProductImageRepo()

    def check_product_duplicate(self, title: str, isbn: int) -> bool:
        if not self.product_repo.get_product_with_title_and_isbn(title=title, isbn=isbn):
            return True
        else:
            raise DuplicateError

    def create_product_and_image(
        self,
        title: str,
        price: int,
        language: str,
        size: str,
        pages: int,
        published_date: str,
        isbn: str,
        description: str,
        issue_number: int,
        product_image_url: str,
        main_category: int,
        sub_category: int,
        main_url: str,
        sub_url: str,
    ) -> bool:
        self.check_product_duplicate(title=title, isbn=isbn)
        with transaction.atomic():
            product = self.product_repo.create_product(
                title=title,
                price=price,
                language=language,
                size=size,
                pages=pages,
                published_date=published_date,
                isbn=isbn,
                description=description,
                issue_number=issue_number,
                product_image_url=product_image_url,
                main_category=main_category,
                sub_category=sub_category,
            )
            self.product_image_repo.create_product_image(
                product_id=product["id"],
                main_url=main_url,
                sub_url=sub_url,
            )
        return True

    def update_product_and_image(
        self,
        product_id: int,
        title: str,
        price: int,
        language: str,
        size: str,
        pages: int,
        published_date: str,
        isbn: str,
        description: str,
        issue_number: int,
        product_image_url: str,
        main_category: int,
        sub_category: int,
        main_url: str,
        sub_url: str,
    ) -> bool:
        self.check_product_duplicate(title=title, isbn=isbn)
        with transaction.atomic():
            self.product_repo.update_product(
                product_id=product_id,
                title=title,
                price=price,
                language=language,
                size=size,
                pages=pages,
                published_date=published_date,
                isbn=isbn,
                description=description,
                issue_number=issue_number,
                product_image_url=product_image_url,
                main_category=main_category,
                sub_category=sub_category,
            )
            self.product_image_repo.update_product_image(
                product_id=product_id,
                main_url=main_url,
                sub_url=sub_url,
            )
        return True

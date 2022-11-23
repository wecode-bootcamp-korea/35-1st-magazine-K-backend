from typing import List

from django.db import transaction

from ..serializers import ProductRepo, ProductImageRepo


class ProductService:
    def __init__(self) -> None:
        self.product_repo = ProductRepo()
        self.product_image_repo = ProductImageRepo()

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

    # TODO 상품 id가 존재하지 않는 것에 대한 요청 유효성 검증 필요
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
        with transaction.atomic():
            product = self.product_repo.update_product(
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
                product_id=product["id"],
                main_url=main_url,
                sub_url=sub_url,
            )
        return True

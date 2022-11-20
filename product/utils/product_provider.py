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
    ) -> List[dict]:
        res = []
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
            res.append(product)
            product_image = self.product_image_repo.create_product_image(
                product_id=product["id"],
                main_url=main_url,
                sub_url=sub_url,
            )
            res.append(product_image)
        return res

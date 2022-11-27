from typing import List

from django.db import transaction

from ..serializers import OrderRepo, OrderItemRepo
from core.exceptions import OutOfRangeError

order_repo = OrderRepo()
order_item_repo = OrderItemRepo()


class CartService:
    """
    장바구니 관련 서비스 로직을 제공하는 클래스
    """

    def add_item_to_cart(self, user_id: int, product_id: int, order_quantity: int) -> bool:
        """
        선택한 상품을 장바구니에 담는 함수
        """
        cart = order_repo.get_order_in_cart_status_or_none(user_id=user_id)
        cart_item = order_item_repo.get_cart_item_or_none(user_id=user_id, product_id=product_id)
        with transaction.atomic():
            if not cart:
                cart = order_repo.create_order(user_id=user_id)
                cart_item = order_item_repo.create_order_item(
                    order_id=cart.id,
                    product_id=product_id,
                    order_quantity=order_quantity,
                )
            if not cart_item:
                order_item_repo.create_order_item(
                    order_id=cart.id,
                    product_id=product_id,
                    order_quantity=order_quantity,
                )
            elif cart_item:
                order_item_repo.update_cart_item_quantity(cart_item=cart_item)
        return True

    def get_cart_list(self, user_id: int) -> List[dict]:
        order_items = order_item_repo.get_cart_items_queryset(user_id=user_id)
        return order_items

    def update_cart_item_quantity(self, user_id: int, product_id: int, calculation: str) -> bool:
        cart_item = order_item_repo.get_cart_item_or_none(user_id=user_id, product_id=product_id)
        if calculation == "subtract" and cart_item.order_quantity == 1:
            raise OutOfRangeError
        order_item_repo.update_cart_item_quantity(cart_item=cart_item, calculation=calculation)
        return True

    def delete_cart_item(self, user_id: int, product_id: int) -> bool:
        cart = order_repo.get_order_in_cart_status_or_none(user_id=user_id)
        return order_item_repo.delete_cart_item(order_id=cart.id, product_id=product_id)

from typing import List

from django.db import transaction

from ..serializers import OrderRepo, OrderItemRepo

order_repo = OrderRepo()
order_item_repo = OrderItemRepo()


class CartService:
    def add_item_to_cart(self, user_id: int, product_id: int, order_quantity: int) -> bool:
        cart = order_repo.get_order_queryset_in_cart_status_or_none(user_id=user_id)
        cart_item = order_item_repo.get_order_item_or_none(user_id=user_id, product_id=product_id)
        if not cart:
            with transaction.atomic():
                order = order_repo.create_order(user_id=user_id)
                order_item_repo.create_order_item(
                    order_id=order.id,
                    product_id=product_id,
                    order_quantity=order_quantity,
                )
        if not cart_item:
            order_item_repo.create_order_item(
                order_id=cart.id,
                product_id=product_id,
                order_quantity=order_quantity,
            )
        if cart_item:
            order_item_repo.update_order_item(cart_item=cart_item)
        return True

    # TODO 장바구니에 물건이 없을 때 반환값 작성 필요
    def get_cart_list(self, user_id: int) -> List[dict]:
        order_items = order_item_repo.get_order_item_list(user_id=user_id)
        return order_items

    def update_cart_item_quantity(self, user_id: int, product_id: int, calculation: str) -> dict:
        cart_item = order_item_repo.get_order_item_or_none(user_id=user_id, product_id=product_id)
        return order_item_repo.update_order_item(cart_item=cart_item, calculation=calculation)

    def delete_cart_item(self, user_id: int, product_id: int) -> bool:
        cart = order_repo.get_order_queryset_in_cart_status_or_none(user_id=user_id)
        return order_item_repo.delete_order_item(order_id=cart.id, product_id=product_id)

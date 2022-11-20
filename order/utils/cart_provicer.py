from django.db import transaction

from ..serializers import OrderRepo, OrderItemRepo

order_repo = OrderRepo()
order_item_repo = OrderItemRepo()


class CartService:
    def add_item_to_cart(self, user_id: int, product_id: int, order_quantity: int) -> bool:
        cart = order_repo.get_order_queryset_in_cart_status(user_id=user_id)
        cart_item = order_item_repo.get_order_item(user_id=user_id, product_id=product_id)
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
                order_id=cart[0].id,
                product_id=product_id,
                order_quantity=order_quantity,
            )
        if cart_item:
            cart_item.order_quantity += order_quantity
            cart_item.save()
        return True

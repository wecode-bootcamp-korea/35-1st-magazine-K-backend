from django.db import transaction

from user.serializers import UserRepo
from ..serializers import OrderRepo, OrderItemRepo

user_repo = UserRepo()
order_repo = OrderRepo()
order_item_repo = OrderItemRepo()


class OrderService:
    """
    상품 주문 관련 서비스 로직을 제공하는 클래스
    """

    def order_items_in_cart(self, user_id: int) -> bool:
        """
        장바구니에 담겨있는 상품을 포인트로 결제하여 주문하는 기능

        장바구니에 담겨있는 모든 상품을 주문합니다. 개별 주문은 아직 구현 전에 있습니다.
        상품 전체 결제금액을 도출하고, 회원의 잔여 포인트 데이터를 가져와 결재합니다.
        배송 관련 기능은 아직 개발되지 않아 결제 즉시 배송완료 상태가 되도록 했습니다.
        """
        total_price = 0
        user_repo.get_user_by_id(user_id=user_id)
        order = order_repo.get_order_in_cart_status_or_none(user_id=user_id)
        order_items = order_item_repo.get_cart_items_with_product(order_id=order.id)

        for order_item in order_items:
            total_price += order_item["order_quantity"] * float(order_item["product"]["price"])

        with transaction.atomic():
            user_repo.deduct_user_point(user_id=user_id, total_price=total_price)
            order_repo.update_order_number(order_id=order.id)
            order_repo.update_order_status_to_delivery_completed(order_id=order.id)

        return True

import uuid

from rest_framework import serializers

from product.serializers import ProductSerializer
from .models import Order, OrderItem, OrderStatus
from .utils.enums import OrderStatusEnum


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderStatusReq(serializers.Serializer):
    order_status = serializers.CharField()


class OrderReq(serializers.Serializer):
    product_id = serializers.IntegerField()
    order_quantity = serializers.IntegerField()


class OrderStatusRepo:
    def __init__(self) -> None:
        pass

    def create_order_status(self, order_status: str) -> object:
        created = OrderStatus.objects.create(order_status=order_status)
        return created

    def get_order_status_by_id(self, order_status_id: int) -> object:
        order_status = OrderStatus.objects.get(id=order_status_id)
        return order_status


class OrderRepo:
    def __init__(self) -> None:
        self.order_status = OrderStatusEnum
        self.order_status_repo = OrderStatusRepo()

    def create_order(self, user_id: int) -> object:
        created = Order.objects.create(
            user_id=user_id,
            order_status=self.order_status_repo.get_order_status_by_id(
                order_status_id=self.order_status.CART.value
            ),
        )
        return created

    def get_order_in_cart_status_or_none(
        self,
        user_id: int,
    ) -> object:
        order = Order.objects.filter(user_id=user_id, order_status=self.order_status.CART.value)
        return order.first()

    def update_order_status_to_delivery_completed(self, order_id: int) -> bool:
        Order.objects.filter(id=order_id).update(
            order_status_id=self.order_status.DELIVERY_COMPLETED.value,
        )
        return True

    def update_order_number(self, order_id: int) -> bool:
        Order.objects.filter(id=order_id).update(order_number=uuid.uuid4())
        return True


class OrderItemRepo:
    """
    장바구니 상품 관련 Repo
    """

    def create_order_item(self, order_id: int, product_id: int, order_quantity: int) -> object:
        created = OrderItem.objects.create(
            product_id=product_id,
            order_id=order_id,
            order_quantity=order_quantity,
        )
        return created

    def get_cart_item_or_none(self, user_id: int, product_id: int) -> object:
        order_item = OrderItem.objects.filter(
            order__user=user_id,
            product_id=product_id,
            order__order_status=OrderStatusEnum.CART.value,
        )
        return order_item.first()

    def get_cart_items_queryset(self, user_id: int) -> dict:
        order_items = OrderItem.objects.filter(
            order__user=user_id,
            order__order_status=OrderStatusEnum.CART.value,
        )
        return OrderItemSerializer(order_items, many=True).data

    def update_cart_item_quantity(self, cart_item: object, calculation: str = "add") -> dict:
        if calculation == "add":
            cart_item.order_quantity += 1
            cart_item.save()
        if calculation == "subtract":
            cart_item.order_quantity -= 1
            cart_item.save()
        return OrderItemSerializer(cart_item).data

    def delete_cart_item(self, order_id: int, product_id: int) -> bool:
        OrderItem.objects.get(order_id=order_id, product_id=product_id).delete()
        return True

    def get_cart_items_with_product(self, order_id: int) -> dict:
        order_items = OrderItem.objects.select_related("product").filter(order_id=order_id)
        return OrderItemSerializer(order_items, many=True).data

    """
    주문 완료된 상품 관련 Repo
    """

    def get_ordered_item_or_none(self, user_id: int, product_id: int) -> object:
        order_item = OrderItem.objects.filter(
            order__user=user_id,
            product_id=product_id,
            order__order_status=OrderStatusEnum.DELIVERY_COMPLETED.value,
        )
        return order_item.first()

from rest_framework import serializers

from .models import Order, OrderItem, OrderStatus
from .utils.enums import OrderStatusEnum


class OrderItemSerializer(serializers.ModelSerializer):
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

    def get_order_queryset_in_cart_status_or_none(
        self,
        user_id: int,
    ) -> object:
        order = Order.objects.filter(user_id=user_id, order_status=self.order_status.CART.value)
        return order.first()


class OrderItemRepo:
    def __init__(self) -> None:
        pass

    def create_order_item(self, order_id: int, product_id: int, order_quantity: int) -> object:
        created = OrderItem.objects.create(
            product_id=product_id,
            order_id=order_id,
            order_quantity=order_quantity,
        )
        return created

    def get_order_item_or_none(self, user_id: int, product_id: int) -> object:
        order_item = OrderItem.objects.filter(
            order__user=user_id,
            product_id=product_id,
            order__order_status=OrderStatusEnum.CART.value,
        )
        return order_item.first()

    def get_order_item_list(self, user_id: int) -> dict:
        order_items = OrderItem.objects.filter(
            order__user=user_id,
            order__order_status=OrderStatusEnum.CART.value,
        )
        return OrderItemSerializer(order_items, many=True).data

    def update_order_item(self, cart_item: object, calculation: str = "add") -> dict:
        if calculation == "add":
            cart_item.order_quantity += 1
            cart_item.save()
        if calculation == "subtract":
            cart_item.order_quantity -= 1
            cart_item.save()
        return OrderItemSerializer(cart_item).data

    def delete_order_item(self, order_id: int, product_id: int) -> bool:
        OrderItem.objects.get(order_id=order_id, product_id=product_id).delete()
        return True

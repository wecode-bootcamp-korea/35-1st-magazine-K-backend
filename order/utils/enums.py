from enum import Enum


class OrderStatusEnum(Enum):
    CART = 1
    BEFORE_DEPOSIT = 2
    PREPARING_FOR_DELIVERY = 3
    SHIPPING = 4
    DELIVERY_COMPLETED = 5
    EXCHANGE = 6
    RETURN = 7

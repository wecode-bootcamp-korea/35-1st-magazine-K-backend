from enum import Enum


class DeliveryStatus(Enum):
    BEFORE_DELIVERY = 0
    SHIPPING_IN_PROGRESS = 1
    DELIVERY_COMPLETED = 2

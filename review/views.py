import json

from enum import Enum

from django.views import View
from django.http import JsonResponse

from core.utils.login_decorator import login_decorator

from review.models import Review
from product.models import Product
from order.models import Order, OrderItem, OrderStatus


class OrderStatusEnum(Enum):
    CART = 1
    BEFORE_DEPOSIT = 2
    PREPARING_FOR_DELIVERY = 3
    SHIPPING = 4
    DELIVERY_COMPLETED = 5
    EXCHANGE = 6
    RETURN = 7


class ReviewView(View):
    @login_decorator
    def post(self, request, product_id):
        try:
            data = json.loads(request.body)
            user = request.user
            content = data["content"]
            rating = data["rating"]
            orderd_products = OrderItem.objects.filter(
                order__user=user,
                order__order_status=OrderStatusEnum.DELIVERY_COMPLETED.value,
                product_id=product_id,
            )

            if not orderd_products.exists():
                return JsonResponse({"MESSAGE": "INVALID_REQUEST"}, status=401)

            Review.objects.create(
                user=user,
                content=content,
                rating=rating,
                product_id=product_id,
            )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id)

        results = [
            {
                "review": review.id,
                "username": review.user.username,
                "content": review.content,
                "rating": review.rating,
            }
            for review in reviews
        ]
        return JsonResponse({"RESULTS": results}, status=200)

    @login_decorator
    def delete(self, request, product_id, review_id):
        try:
            user = request.user
            review = Review.objects.get(id=review_id, user=user, product=product_id)

            review.delete()
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=204)

        except Review.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID_REVIEW"}, status=401)

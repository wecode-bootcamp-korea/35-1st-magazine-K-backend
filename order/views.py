from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse

from .serializers import OrderReq, OrderStatusReq, OrderStatusRepo
from .utils.cart_provicer import CartService
from .utils.order_provider import OrderService
from core.login_decorator import login_decorator

cart_service = CartService()
order_service = OrderService()
order_status_repo = OrderStatusRepo()


class CartAPI(APIView):
    @login_decorator
    def post(self, request):
        user = request.user
        params = request.data
        serializer = OrderReq(data=params)
        serializer.is_valid(raise_exception=True)
        cart_service.add_item_to_cart(user_id=user["id"], **serializer.data)
        return JsonResponse({"msg": "Created"}, status=status.HTTP_201_CREATED)

    @login_decorator
    def get(self, request):
        user = request.user
        cart_items = cart_service.get_cart_list(user_id=user["id"])
        return JsonResponse({"res": cart_items}, status=status.HTTP_200_OK)

    @login_decorator
    def put(self, request, product_id: int, calculation: str = "add"):
        user = request.user
        cart_service.update_cart_item_quantity(
            user_id=user["id"],
            product_id=product_id,
            calculation=calculation,
        )
        return JsonResponse({"msg": "Updated"}, status=status.HTTP_200_OK)

    @login_decorator
    def delete(self, request, product_id: int):
        user = request.user
        cart_service.delete_cart_item(user_id=user["id"], product_id=product_id)
        return JsonResponse({"msg": "Deleted"}, status=status.HTTP_200_OK)


class OrderAPI(APIView):
    @login_decorator
    def put(self, request):
        user = request.user
        order_service.order_items_in_cart(user_id=user["id"])
        return JsonResponse({"msg": "Created"}, status=status.HTTP_200_OK)


class OrderStatusAPI(APIView):
    def post(self, request):
        params = request.data
        serializer = OrderStatusReq(data=params)
        serializer.is_valid(raise_exception=True)
        order_status_repo.create_order_status(**serializer.data)
        return JsonResponse({"msg": "Created"}, status=status.HTTP_201_CREATED)

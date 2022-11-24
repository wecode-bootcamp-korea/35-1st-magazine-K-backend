from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse

from core.login_decorator import login_decorator
from .serializers import ReviewReq, ReviewUpdateReq
from .utils.review_provider import ReviewService

review_service = ReviewService()


class ReviewAPI(APIView):
    @login_decorator
    def post(self, request, product_id):
        user = request.user
        params = request.data
        serializer = ReviewReq(data=params)
        serializer.is_valid(raise_exception=True)
        review_service.create_review(product_id=product_id, user_id=user["id"], **serializer.data)
        return JsonResponse({"msg": "Created"}, status=status.HTTP_201_CREATED)

    def get(self, request, product_id):
        reviews = review_service.get_review_list(product_id=product_id)
        return JsonResponse({"res": reviews}, status=status.HTTP_200_OK)

    @login_decorator
    def put(self, request, review_id: int):
        user = request.user
        params = request.data
        serializer = ReviewUpdateReq(data=params)
        serializer.is_valid(raise_exception=True)
        review_service.update_review(user_id=user["id"], review_id=review_id, **serializer.data)
        return JsonResponse({"msg": "Updated"}, status=status.HTTP_200_OK)

    @login_decorator
    def delete(self, request, review_id: int):
        user = request.user
        review_service.delete_review(user_id=user["id"], review_id=review_id)
        return JsonResponse({"msg": "Deleted"}, status=status.HTTP_200_OK)

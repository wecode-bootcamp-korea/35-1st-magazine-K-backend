from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse

from .serializers import CategoryRepo, ProductRepo, ProductReq, CategoryReq

category_repo = CategoryRepo()
product_repo = ProductRepo()


@api_view(["GET"])
def get_product_list(request):
    category = int(request.GET.get("category", 1))
    sort_by = request.GET.get("sort_by", "latest_issue")
    keyword = request.GET.get("keyword", "")
    offset = int(request.GET.get("offset", 0))
    limit = int(request.GET.get("limit", 0))
    product_list = product_repo.get_product_list(
        category=category,
        sort_by=sort_by,
        keyword=keyword,
        offset=offset,
        limmit=limit,
    )
    return JsonResponse({"res": product_list, "status": status.HTTP_200_OK})


class CategoryAPI(APIView):
    def get(self, request):
        category_list = category_repo.get_category_list()
        return JsonResponse({"res": category_list, "status": status.HTTP_200_OK})

    def post(self, request):
        params = request.data
        serializer = CategoryReq(data=params)
        serializer.is_valid(raise_exception=True)
        created = category_repo.create_category(**serializer.data)
        return JsonResponse({"status": status.HTTP_201_CREATED})

    def put(self, request, category_id: int):
        params = request.data
        serializer = CategoryReq(data=params)
        serializer.is_valid(raise_exception=True)
        updated = category_repo.update_category(category_id=category_id, **serializer.data)
        return JsonResponse({"status": status.HTTP_200_OK})

    def delete(self, request, category_id: int):
        deleted = category_repo.delete_category(category_id=category_id)
        return JsonResponse({"status": status.HTTP_200_OK})


class ProductAPI(APIView):
    def post(self, request):
        params = request.data
        serializer = ProductReq(data=params)
        serializer.is_valid(raise_exception=True)
        created = product_repo.create_product(**serializer.data)
        return JsonResponse({"status": status.HTTP_201_CREATED})

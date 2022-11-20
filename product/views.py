from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse

from .serializers import CategoryRepo, ProductRepo, ProductReq, CategoryReq
from .utils.product_provider import ProductService

category_repo = CategoryRepo()
product_repo = ProductRepo()
product_service = ProductService()


class CategoryAPI(APIView):
    def post(self, request):
        params = request.data
        serializer = CategoryReq(data=params)
        serializer.is_valid(raise_exception=True)
        created = category_repo.create_category(**serializer.data)
        return JsonResponse({"status": status.HTTP_201_CREATED})

    def get(self, request):
        category_list = category_repo.get_category_list()
        return JsonResponse({"res": category_list, "status": status.HTTP_200_OK})

    def put(self, request, category_id: int):
        params = request.data
        serializer = CategoryReq(data=params)
        serializer.is_valid(raise_exception=True)
        updated = category_repo.update_category(category_id=category_id, **serializer.data)
        return JsonResponse({"status": status.HTTP_200_OK})

    def delete(self, request, category_id: int):
        deleted = category_repo.delete_category(category_id=category_id)
        return JsonResponse({"status": status.HTTP_200_OK})


# TODO 일대일 관계 역참조 테이블 직렬화 관련 이슈
@api_view(["GET"])
def get_product_list(request):
    category = request.GET.get("category", 1)
    sort_by = request.GET.get("sort_by", "latest_issue")
    keyword = request.GET.get("keyword", "")
    offset = request.GET.get("offset", 0)
    limit = request.GET.get("limit", 10)
    product_list = product_repo.get_product_and_image_list_with_filter(
        category=category,
        sort_by=sort_by,
        keyword=keyword,
        offset=offset,
        limmit=limit,
    )
    return JsonResponse({"res": product_list, "status": status.HTTP_200_OK})


class ProductAPI(APIView):
    def get(self, request, product_id: int):
        product = product_repo.get_product_detail(product_id=product_id)
        return JsonResponse({"res": product, "status": status.HTTP_200_OK})

    def post(self, request):
        params = request.data
        serializer = ProductReq(data=params)
        serializer.is_valid(raise_exception=True)
        product_service.create_product_and_image(**serializer.data)
        return JsonResponse({"status": status.HTTP_201_CREATED})

    def put(self, request, product_id: int):
        params = request.data
        serializer = ProductReq(data=params)
        serializer.is_valid(raise_exception=True)
        product_repo.update_product_and_image(product_id=product_id, **serializer.data)
        return JsonResponse({"status": status.HTTP_200_OK})

    def delete(self, request, product_id: int):
        product_repo.delete_product_and_image(product_id=product_id)
        return JsonResponse({"status": status.HTTP_200_OK})

import json

from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import FieldError

from product.models import Category, Product, ProductImage


class ProductView(View):
    def get(self, request):
        try:
            category = int(request.GET.get("category", 1))
            offset = int(request.GET.get("offset", 0))
            limit = int(request.GET.get("limit", 0))
            sort_by = request.GET.get("sort_by", "latest_issue")
            keyword = request.GET.get("keyword", "").upper()

            sort_options = {
                "latest_issue": "-issue_number",
                "oldest_issue": "issue_number",
                "high_price": "-price",
                "low_price": "price",
            }

            filter_options = Q()

            if category:
                filter_options |= Q(main_category=category)
                filter_options |= Q(sub_category=category)

            if keyword:
                filter_options &= Q(title__icontains=keyword)

            products = (
                Product.objects.filter(filter_options)
                .order_by(sort_options[sort_by])
                .select_related("productimage")
            )

            result = [
                {
                    "total_count": products.count(),
                    "products": [
                        {
                            "product_id": product.id,
                            "title": product.title,
                            "issue_number": product.issue_number,
                            "main_category": product.main_category.name,
                            "price": product.price,
                            "main_img_url_1": product.productimage.main_url,
                            "main_img_url_2": product.productimage.sub_url,
                        }
                        for product in products[offset : offset + limit]
                    ],
                }
            ]

            return JsonResponse({"result": result}, status=200)

        except FieldError:
            return JsonResponse({"message": "QUARY_PARAMETER_ERROR"}, status=400)


class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            results = {
                "category": product.main_category.name,
                "issue_number": product.issue_number,
                "title": product.title,
                "price": product.price,
                "language": product.language,
                "size": product.size,
                "pages": product.pages,
                "published_date": product.published_date,
                "isbn": product.isbn,
                "description": product.description,
                "product_image_url": product.product_image_url,
            }
            return JsonResponse({"RESULTS": results}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID_PRODUCT"}, status=404)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)


class ProductManageView(View):
    def post(self, request):
        data = json.loads(request.body)

        Product.objects.create(
            title="더미 데이터",
            price=20000,
            language="KOREAN",
            size="170 x 240 mm",
            pages=200,
            published_date="20xx. xx. xx.",
            isbn="979-11-xxxxxx-x-x",
            description="더미 데이터",
            issue_number=data["issue_number"],
            product_image_url="http://placeimg.com/640/480/any",
            main_category=Category.objects.get(id=1),
            sub_category=Category.objects.get(id=data["sub_category"]),
        )
        ProductImage.objects.create(
            product=Product.objects.get(id=data["product_id"]),
            main_url="http://placeimg.com/640/480/any",
            sub_url="http://placeimg.com/640/480/any",
        )

        return JsonResponse({"message": "success"}, status=202)

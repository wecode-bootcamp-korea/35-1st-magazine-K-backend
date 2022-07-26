from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q
from django.core.exceptions import FieldError

from products.models import Product

class ProductView(View):
    def get(self, request):
        try:
            category = int(request.GET.get('category', 1))
            offset   = int(request.GET.get('offset', 0))
            limit    = int(request.GET.get('limit', 0))
            sort_by  = request.GET.get('sort_by', '-issue_number')

            products = Product.objects.filter(Q(main_category=category) | Q(sub_category=category))

            sorted_products = products.order_by(sort_by)

            result = [
                {
                    'product_id'    : product.id,
                    'title'         : product.title,
                    'issue_number'  : product.issue_number,
                    'main_category' : product.main_category.name,
                    'price'         : product.price,
                    'main_img_url_1': product.productimage.main_url,
                    'main_img_url_2': product.productimage.sub_url,
                }
                for product in sorted_products[offset:offset+limit]]

            result.append(
                {
                    'category_total' : len(products)
                }
            )

            return JsonResponse({'result' : result}, status = 200)

        except FieldError:
            return JsonResponse({'message' : 'QUARY_PARAMETER_ERROR'}, status = 400)
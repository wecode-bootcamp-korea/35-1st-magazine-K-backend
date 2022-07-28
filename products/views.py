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
            sort_by  = request.GET.get('sort_by', 'latest_issue')

            sort_options = {
                'latest_issue' : '-issue_number',
                'oldest_issue' : 'issue_number',
                'high_price'   : '-price',
                'low_price'    : 'price',
            }

            filter_options = Q()

            if category:
                filter_options |= Q(main_category=category)
                filter_options |= Q(sub_category=category)

            products = Product.objects.filter(filter_options).order_by(sort_options[sort_by])

            result = [{
                'total_count' : products.count(),
                'products' : [{
                    'product_id'    : product.id,
                    'title'         : product.title,
                    'issue_number'  : product.issue_number,
                    'main_category' : product.main_category.name,
                    'price'         : product.price,
                    'main_img_url_1': product.productimage.main_url,
                    'main_img_url_2': product.productimage.sub_url,
                }for product in products[offset:offset+limit]]
            }]

            return JsonResponse({'result' : result}, status = 200)

        except FieldError:
            return JsonResponse({'message' : 'QUARY_PARAMETER_ERROR'}, status = 400)

class ProductDetailView(View):
    def get(self, request, product_id):
        try :
            product  = Product.objects.get(id=product_id)

            results = {
                    'category'         : product.main_category.name,
                    'issue_number'     : product.issue_number,
                    'title'            : product.title,
                    'price'            : product.price,
                    'language'         : product.language,
                    'size'             : product.size,
                    'pages'            : product.pages,
                    'published_date'   : product.published_date,
                    'isbn'             : product.isbn,
                    'description'      : product.description,
                    'product_image_url': product.product_image_url,
                }
            return JsonResponse({'RESULTS':results}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_PRODUCT'}, status=404)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

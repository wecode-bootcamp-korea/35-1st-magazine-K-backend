from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from products.models import Product

class ProductView(View):
    def get(self, request):
        category = int(request.GET.get('category', 1))
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 0))
        sort     = int(request.GET.get('sort', 0))

        products = Product.objects.filter(categoryproduct__category_id=category)

        if sort == 0:
            sorted_products = products.order_by('-issue_number')
        elif sort == 1:
            sorted_products = products.order_by('issue_number')
        elif sort == 2:
            sorted_products = products.order_by('-price')
        elif sort == 3:
            sorted_products = products.order_by('price')

        result = [
            {
                'title'         : product.title,
                'issue_number'  : product.issue_number,
                'main_category' : product.category.get(id=category).name,
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
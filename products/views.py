from django.views import View
from django.http import JsonResponse

from products.models import Product

class ProductView(View):
    def get(self, request):
        category = int(request.GET.get('category', 1))
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 0))
        sort     = int(request.GET.get('sort', 0))

        if sort == 0:
            products = Product.objects.filter(categoryproduct__category_id=category).order_by('-issue_number')
        elif sort == 1:
            products = Product.objects.filter(categoryproduct__category_id=category).order_by('issue_number')
        elif sort == 2:
            products = Product.objects.filter(categoryproduct__category_id=category).order_by('-price')
        elif sort == 3:
            products = Product.objects.filter(categoryproduct__category_id=category).order_by('price')

        result = [
            {
                'title'         : product.title,
                'issue_number'  : product.issue_number,
                'main_category' : product.category.get(id=category).name,
                'price'         : product.price,
                'main_img_url_1': product.productimage.main_url,
                'main_img_url_2': product.productimage.sub_url,
            }
            for product in products[offset:limit]]

        result.append(
            {
                'cate_total' : len(products)
            }
        )

        return JsonResponse({'result' : result}, status = 200)
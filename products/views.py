from django.views     import View
from django.http      import JsonResponse

from products.models import Product

class ProductView(View):
    def get(self, request):
        category = int(request.GET.get('category', 1))
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 0))
        sort_by  = request.GET.get('sort_by', 'newest')

        products = Product.objects.filter(categoryproduct__category_id=category)

        if sort_by == 'newest':
            sorted_products = products.order_by('-issue_number')

        if sort_by == 'oldest':
            sorted_products = products.order_by('issue_number')

        if sort_by == 'high_to_low':
            sorted_products = products.order_by('-price')

        if sort_by == 'low_to_high':
            sorted_products = products.order_by('price')

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
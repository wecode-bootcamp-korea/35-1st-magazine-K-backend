from django.views     import View
from django.http      import JsonResponse

from products.models  import Product

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
from unicodedata import category
from django.views     import View
from django.http      import JsonResponse

from products.models import Category, Product

class ProductDetailView(View):
    def get(self, request, category_id, product_id):
        try :
            product       = Product.objects.get(id=product_id)
            category      = Category.objects.get(id=category_id)
            category_name = Product.objects.filter(id=product_id).values('category__name')

            # if not Category.objects.filter(id=category_id).exists:
            #     return JsonResponse({'MESSAGE':'INVALID_CATEGORY_e'}, status=404)
            
            results = {
                    'category'         : category_name[0]['category__name'],
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
            
        except Category.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_CATEGORY'}, status=404)

        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_PRODUCT'}, status=404)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
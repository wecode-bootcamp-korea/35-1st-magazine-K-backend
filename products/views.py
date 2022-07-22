from django.views    import View
from django.http     import JsonResponse
from products.models import Category, Product

class ProductDetailView(View):
    def get(self, request):
        try :
            issue_number = int(request.GET.get('issue', None))
            category     = int(request.GET.get('category', None))
            product      = Product.objects.get(issue_number=issue_number)
            category     = Category.objects.get(id=category)
            results      = [
                {
                    'category'         : category.name,
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
            ]
            return JsonResponse({'RESULTS' : results}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_PRODUCT'}, status=400)
    
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)


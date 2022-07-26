import json

from django.views               import View
from django.http                import JsonResponse

from core.utils.login_decorator import login_decorator
from comments.models            import Comment
from products.models            import Product

class CommentView(View):
    @login_decorator
    def post(self, request, product_id):
        try :  
            data    = json.loads(request.body)
            user    = request.user
            content = data['content'] 
            rating  = data['rating']

            Comment.objects.create(
                user_id    = user.id,
                content    = content,
                rating     = rating,
                product_id = product_id,
            ) 
            return JsonResponse({'MESSAGE':'SUCCESE'}, status=200)

        except Product.DoesNotExist: 
            return JsonResponse({'MESSAGE':'INVALID_PRODUCT'}, status=404)

        except KeyError: 
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

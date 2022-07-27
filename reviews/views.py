import json

from django.views               import View
from django.http                import JsonResponse

from core.utils.login_decorator import login_decorator
from comments.models            import Comment
from products.models            import Product

class CommentView(View):
    def get(self, request, product_id):
        try:
            comments = Comment.objects.filter(product_id=product_id)
    
            results = [{
                        'review'  : comment.id,
                        'username': comment.user.username,
                        'content' : comment.content,
                        'rating'  : comment.rating,
                         }for comment in comments]
            return JsonResponse({'RESULTS':results}, status=200)      

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400) 
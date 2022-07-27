import json

from django.views               import View
from django.http                import JsonResponse

from reviews.models             import Review
from products.models            import Product

class ReviewView(View):
    def get(self, request, product_id):
        try:
            reviews = Review.objects.filter(product_id=product_id)
    
            results = [{
                        'review'  : review.id,
                        'username': review.user.username,
                        'content' : review.content,
                        'rating'  : review.rating,
                         }for review in reviews]
            return JsonResponse({'RESULTS':results}, status=200)      

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400) 
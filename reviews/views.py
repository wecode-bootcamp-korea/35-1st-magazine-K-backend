import json

from django.views               import View
from django.http                import JsonResponse

from core.utils.login_decorator import login_decorator

from reviews.models             import Review
from products.models            import Product

class ReviewView(View):
    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id)
    
        results = [{
                    'review'  : review.id,
                    'username': review.user.username,
                    'content' : review.content,
                    'rating'  : review.rating,
                    }for review in reviews]
        return JsonResponse({'RESULTS':results}, status=200)      
        
    @login_decorator   
    def delete(self, request, product_id, review_id):
        try:
            user   = request.user
            review = Review.objects.get(id=review_id, user=user, product=product_id)

            review.delete()
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=204)

        except Review.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_REVIEW'}, status=401)
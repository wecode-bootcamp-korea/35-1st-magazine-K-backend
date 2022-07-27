import json

from django.views               import View
from django.http                import JsonResponse

from core.utils.login_decorator import login_decorator

from reviews.models             import Review

class ReviewView(View):
    @login_decorator   
    def delete(self, request, product_id, review_id):
        try:
            user   = request.user
            review = Review.objects.get(id=review_id, user=user, product=product_id)

            review.delete()
            return JsonResponse({'MESSAGE':'SUCCESE'}, status=200)

        except Review.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_REVIEW'}, status=400)
                          
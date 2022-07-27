import json
from enum             import Enum
from django.views     import View
from django.http      import JsonResponse
from reviews.models       import Review
from products.models      import Product
from orders.models        import Order, OrderStatus, OrderItem
from core.utils.login_decorator import login_decorator

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

class ReviewView(View):
    @login_decorator
    def post(self, request, product_id):
        try:
            data            = json.loads(request.body)
            user            = request.user
            content         = data['content']
            rating          = data['rating']
            orderd_products = OrderItem.objects.filter(order__user=user, order__order_status=OrderStatusEnum.DELIVERY_COMPLETED.value, product_id=product_id)
            if not orderd_products.exists():
                return JsonResponse({'MESSAGE':'INVALID_REQUEST'}, status=401)
            Review.objects.create(
                user       = user,
                content    = content,
                rating     = rating,
                product_id = product_id,
            )
            return JsonResponse({'MESSAGE':'SUCCESE'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
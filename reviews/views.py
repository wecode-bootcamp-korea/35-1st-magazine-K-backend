import json

from django.views               import View
from django.http                import JsonResponse

from core.utils.login_decorator import login_decorator

from reviews.models             import Review
from products.models            import Product  
from orders.models              import Order, OrderStatus, OrderItem

class ReviewView(View):
    @login_decorator
    def post(self, request, product_id):
        try:
            data            = json.loads(request.body)
            user            = request.user
            content         = data['content']
            rating          = data['rating']
            
            delivered       = OrderStatus.objects.get(id=5)
            orderd_products = OrderItem.objects.filter(order__user=user, order__order_status=delivered, product_id=product_id)
            
            if not orderd_products.exists():
                return JsonResponse({'MESSAGE':'INVALID_REQUEST'}, status=401)

            Review.objects.create(
                user_id    = user.id,
                content    = content,
                rating     = rating,
                product_id = product_id,
            )
            return JsonResponse({'MESSAGE':'SUCCESE'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
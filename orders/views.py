import json

from django.views import View
from django.http  import JsonResponse

from core.utils.login_decorator import login_decorator
from orders.models import Order

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            user         = request.user
            order_status = data['order_status']

            Order.objects.create(
                user         = user,
                order_status = order_status
            )
            
            return JsonResponse({'message' : 'SUCCESE'}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
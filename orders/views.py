import json

from django.views import View
from django.http  import JsonResponse

from core.utils.login_decorator import login_decorator
from orders.models import Order, OrderItem

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            user         = request.user
            order_status = 1
            product      = data['product'] # 해당 제품 product_id 값

            if Order.objects.filter(order_status=1).exists():
                if OrderItem.objects.filter(product=product).exists():
                    OrderItem.objects.filter(product=product).update(order_quantity=('order_quantity') + 1) # 기존 데이터에 값을 연산할 수 있는 메소드를 찾을 수 없음
                else:
                    OrderItem.objects.create(
                        product = product,
                        order = Order.objects.get(order_status=1).id,
                        order_quantity = 1,
                        order_price = OrderItem.objects.get(product=product).product.price
                    )
            else:
                Order.objects.create(
                    user = user,
                    order_status = order_status
                )
                OrderItem.objects.create(
                    product = product,
                    order = Order.objects.get(order_status=1).id,
                    order_quantity = 1,
                    order_price = OrderItem.objects.get(product=product).product.price
                )

            items = OrderItem.objects.filter(order__user_id=user)

            result = [{
                'title' : item.product.title,
                'price' : item.order_price,
                'quantity' : item.order_quantity,
            } for item in items]
   
            return JsonResponse({'result' : result}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    @login_decorator
    def patch(self, request):
        try:
            data = json.loads(request.body)

            product = data['product'] # 해당 제품 product_id 값
            order   = data['order'] # 해당 주문 product_id 값

            OrderItem.objects.update(
                count = OrderItem.objects.filter(order=order, product=product).update()
            )

            return JsonResponse({'result' : })
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
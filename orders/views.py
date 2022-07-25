import json

from django.views import View
from django.http  import JsonResponse

from core.utils.login_decorator import login_decorator
from orders.models              import Order, OrderItem, OrderStatus
from products.models            import Product
from users.models               import User

class CartView(View):
    @login_decorator
    def get(self, request):
        '''
        카트 상태의 상품 조회

        - 장바구니 모달창 또는 장바구니 페이지로 이동시 해당 유저의 장바구니 상품 조회
        - http://localhost:8000/orders/cart
        '''
        user = request.user
        CART_STATUS = 1

        user_cart = Order.objects.filter(user=user.id).get(order_status=CART_STATUS).orderitem_set.all()

        result = [{
            'title'   : order.product.title,
            'price'   : order.order_price,
            'quantity': order.order_quantity,
            'picture' : order.product.productimage.main_url
        } for order in user_cart]

        return JsonResponse({'result' : result}, status = 200)

    @login_decorator
    def post(self, request):
        '''
        제품 카트에 담기

        - 웹 사이트 상에서 `ADD TO CART` 버튼 클릭 시 카트에 해당 상품을 담기
        - http://localhost:8000/orders/cart
        '''
        try:
            data = json.loads(request.body)

            user         = request.user
            product      = data['product']
            CART_STATUS = 1

            selected_product = Product.objects.get(id=product)
            

            if Order.objects.filter(user=User.objects.get(id=user.id), order_status=CART_STATUS).exists():
                if OrderItem.objects.filter(product=product, order=Order.objects.filter(user=user.id).get(order_status=CART_STATUS).id).exists():
                    ordered_item = OrderItem.objects.filter(product=product, order=Order.objects.filter(user=user.id).get(order_status=CART_STATUS).id)
                    ordered_item.update(order_quantity=OrderItem.objects.filter(product=product).get(order=Order.objects.filter(user=user.id).get(order_status=CART_STATUS).id).order_quantity + 1)
                else:
                    OrderItem.objects.create(
                        product        = selected_product,
                        order          = Order.objects.get(user=user.id),
                        order_quantity = 1,
                        order_price    = selected_product.price
                    )
            else:
                Order.objects.create(
                    user         = User.objects.get(id=user.id),
                    order_status = OrderStatus.objects.get(id = CART_STATUS)
                )
                OrderItem.objects.create(
                    product        = selected_product,
                    order          = Order.objects.get(user=user.id),
                    order_quantity = 1,
                    order_price    = selected_product.price
                )

            items = OrderItem.objects.filter(order__user_id=user)

            result = [{
                'title'   : item.product.title,
                'price'   : item.order_price,
                'quantity': item.order_quantity,
                'picture' : item.product.productimage.main_url
            } for item in items]
   
            return JsonResponse({'result' : result}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    @login_decorator
    def patch(self, request):
        '''
        장바구니에 올라간 상품 수량 증감

        - 웹 사이트의 장바구니 모달창 또는 장바구니 페이지에서 '+', '-' 버튼으로 상품 개수 증감
        - http://localhost:8000/orders/cart
        '''
        try:
            data = json.loads(request.body)

            user        = request.user
            product     = data['product']     # 해당 제품 product_id 값
            calculation = data['calculation'] # 제품을 더할 것인지, 뺄 것인지 구분 (1 = 더하기, 0 = 빼기)
            CART_STATUS = 1

            pick_products = OrderItem.objects.filter(order=Order.objects.filter(user=user.id).get(order_status=CART_STATUS), product=product)
            pick_product  = OrderItem.objects.filter(order=Order.objects.filter(user=user.id).get(order_status=CART_STATUS)).get(product=product)

            if calculation == 1:
                pick_products.update(
                    order_quantity=(pick_product.order_quantity + 1) # 상품 개수 증가
                )
            elif calculation == 0:
                pick_products.update(
                    order_quantity=(pick_product.order_quantity - 1) # 상품 개수 감소
                )

            result = {'order_quantity' : OrderItem.objects.filter(order=Order.objects.filter(user=user.id).get(order_status=CART_STATUS)).get(product=product).order_quantity}

            return JsonResponse({'result' : result}, status = 200)
        
        except OrderItem.DoesNotExist:
            return JsonResponse({'message' : 'DATA_NOT_EXIST'}, status = 400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    @login_decorator
    def delete(self, request, product):
        '''
        장바구니에 올라간 상품 삭제
        
        - http://localhost:8000/orders/cart
        '''
        try:
            user = request.user
            CART_STATUS = 1

            OrderItem.objects.filter(order=Order.objects.filter(user=user.id).get(order_status=CART_STATUS).id, product=product).delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except OrderItem.DoesNotExist:
            return JsonResponse({'message' : 'DATA_NOT_EXIST'}, status = 400)
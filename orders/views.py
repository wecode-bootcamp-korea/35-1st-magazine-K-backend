import json

from django.views import View
from django.http  import JsonResponse

from core.utils.login_decorator import login_decorator
from orders.models import Order, OrderItem

class CartView(View):
    @login_decorator
    def post(self, request):
        '''
        제품 카트에 담기

        - 웹 사이트 상에서 `ADD TO CART` 버튼 클릭 시 카트에 해당 상품을 담기
        - http://localhost:8000/orders/cart
        '''
        try:
            data = json.loads(request.body)

            user         = request.user    # login_decorator를 통해 토큰을 검사하여 로그인
            product      = data['product'] # 해당 상품의 product_id 값
            ORDER_STATUS = 1               # 장바구니 상태를 뜻하는 상수 (1 == 장바구니, 2 == 입금전 ....)

            check_status  = Order.objects.get(order_status=ORDER_STATUS).id               # 주문 건이 장바구니 상태인지 확인을 위한 변수
            check_product = OrderItem.objects.filter(product=product, order=check_status) # 클라이언트가 요청한 물품이 장바구니 상태의 물품인지 확인하기 위한 변수

            if Order.objects.filter(order_status=ORDER_STATUS).exists():                         # 장바구니 상태의 주문이 존재하는지 확인한다.
                if check_product.exists():                                                       # 존재한다면 카트에 담을 상품이 장바구니에 있는지 확인한다.
                    check_product.update(order_quantity=(OrderItem.objects.get(id=product) + 1)) # 있다면 기존에 생성된 상품 수량에 1개 더해준다.
                else:
                    # 카트에 클라이언트가 담을 상품이 존재하지 않는다면 신규로 생성한다.
                    OrderItem.objects.create(
                        product        = product,
                        order          = Order.objects.get(order_status=1).id,
                        order_quantity = 1,
                        order_price    = check_product.product.price
                    )
            else:
                # 장바구니에 상품이 존재하지 않는다면 신규 주문과 상품을 생성한다.
                Order.objects.create(
                    user         = user,
                    order_status = ORDER_STATUS
                )
                OrderItem.objects.create(
                    product        = product,
                    order          = Order.objects.get(order_status=1).id,
                    order_quantity = 1,
                    order_price    = check_product.product.price
                )

            items = OrderItem.objects.filter(order__user_id=user) # 클라이언트에 생성 혹은 수정된 장바구니 상품 정보를 전달하기 위한 Queryset 생성

            result = [{
                'title'   : item.product.title,
                'price'   : item.order_price,
                'quantity': item.order_quantity,
            } for item in items]
   
            return JsonResponse({'result' : result}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    @login_decorator
    def patch(self, request):
        '''
        장바구니에 올라간 물품의 수량 증감

        - 웹 사이트의 장바구니 모달창 또는 장바구니 페이지에서 '+', '-' 버튼으로 상품 개수 증감
        - http://localhost:8000/orders/cart
        '''
        try:
            data = json.loads(request.body)

            product     = data['product']     # 해당 제품 product_id 값
            order       = data['order']       # 해당 주문 product_id 값
            calculation = data['calculation'] # 제품을 더할 것인지, 뺄 것인지 구분 (1 = 더하기, 0 = 빼기)

            check = OrderItem.objects.filter(order=order, product=product)

            if calculation == 1:
                OrderItem.objects.update(
                    count = check.update(order_quantity=(OrderItem.objects.get(id=product) + 1)) # 상품 개수 증가
                )
            elif calculation == 0:
                OrderItem.objects.update(
                    count = check.update(order_quantity=(OrderItem.objects.get(id=product) - 1)) # 상품 개수 감소
                )

            result = {'order_quantity' : OrderItem.objects.get(product=product, order=order)}

            return JsonResponse({'result' : result}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
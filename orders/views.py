from enum import Enum
import uuid
import json

from django.views     import View
from django.http      import JsonResponse
from django.db        import transaction

from core.utils.login_decorator import login_decorator
from orders.models              import Order, OrderItem
from products.models            import Product
from users.models               import User

class OrderStatusEnum(Enum):
    CART                   = 1
    BEFORE_DEPOSIT         = 2
    PREPARING_FOR_DELIVERY = 3
    SHIPPING               = 4
    DELIVERY_COMPLETED     = 5
    EXCHANGE               = 6
    RETURN                 = 7

class CartView(View):
    @login_decorator
    def get(self, request):
            user          = request.user
            cart_products = OrderItem.objects.filter(order__user=user, order__order_status=OrderStatusEnum.CART.value)

            if not cart_products.exists():
                return JsonResponse({'message' : 'EMPTY CART'}, status = 404)

            result = [{
                'user_point' : user.point,
                'product' : [{
                    'product_id': cart_product.product.id,
                    'title'     : cart_product.product.title,
                    'price'     : cart_product.product.price,
                    'quantity'  : cart_product.order_quantity,
                    'picture'   : cart_product.product.productimage.main_url
            } for cart_product in cart_products]
            }]

            return JsonResponse({'result' : result}, status = 200)
        
    @login_decorator
    def post(self, request, product_id):
        try:
            data          = json.loads(request.body)
            user          = request.user
            quantity      = data['quantity']
            DEFAULT_VALUE = 0

            selected_product = Product.objects.get(id=product_id)
            cart_order       = Order.objects.filter(user=user, order_status=OrderStatusEnum.CART.value)
            cart_products    = OrderItem.objects.filter(order__user=user, product_id=selected_product, order__order_status=OrderStatusEnum.CART.value)

            with transaction.atomic():
                if not cart_order.exists():
                    new_order = Order.objects.create(
                        user            = user,
                        order_status_id = OrderStatusEnum.CART.value
                    )
                    OrderItem.objects.create(
                        product        = selected_product,
                        order          = new_order,
                        order_quantity = DEFAULT_VALUE,
                    )

                if not cart_products.exists():
                    OrderItem.objects.create(
                    product        = selected_product,
                    order          = cart_order.first(),
                    order_quantity = DEFAULT_VALUE,
                )

                cart_product = cart_products.first()
                cart_product.order_quantity += quantity
                cart_product.save()
                
            return JsonResponse({'result' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    @login_decorator
    def patch(self, request, product_id):
        try:
            data        = json.loads(request.body)
            user        = request.user
            calculation = data['calculation']

            selected_product = Product.objects.get(id=product_id)
            cart_product     = OrderItem.objects.filter(order__user=user, product_id=selected_product, order__order_status=OrderStatusEnum.CART.value)

            if calculation == 'addition':
                cart_product.update(order_quantity=cart_product.first().order_quantity + 1)

            if calculation == 'subtraction':
                if cart_product.first().order_quantity == 1:
                    return JsonResponse({'message' : "CAN'T_SUBTRACTION"}, status = 400)
                else:
                    cart_product.update(order_quantity=cart_product.first().order_quantity - 1)

            return JsonResponse({'result' : 'SUCCESS'}, status = 200)
        
        except OrderItem.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_NOT_EXIST'}, status = 404)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    @login_decorator
    def delete(self, request, product_id):
        try:
            user         = request.user
            cart_product = OrderItem.objects.get(order__user=user, product_id=product_id, order__order_status_id=OrderStatusEnum.CART.value)

            cart_product.delete()

            if not Order.objects.get(user=user, order_status_id=OrderStatusEnum.CART.value).orderitem_set.exists():
                Order.objects.get(user=user, order_status_id=OrderStatusEnum.CART.value).delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except Order.DoesNotExist:
            return JsonResponse({'message' : 'ORDER_NOT_EXIST'}, status = 404)
        except Order.MultipleObjectsReturned:
            return JsonResponse({'message' : 'DATA_INTEGRITY_ERROR'}, status = 400)
        except OrderItem.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_NOT_EXIST'}, status = 404)

class OrderView(View):
    @login_decorator
    def patch(self, request):
        try:
            data        = json.loads(request.body)
            user        = request.user
            price_total = data['price_total']

            user_cart = Order.objects.filter(user=user, order_status=OrderStatusEnum.CART.value)
            
            with transaction.atomic():
                if not user_cart.exists():
                    return JsonResponse({'message' : 'PRODUCT_NOT_EXIST'}, status = 404)

                User.objects.filter(id=user.id).update(point=User.objects.get(id=user.id).point - price_total)
                user_cart.update(order_number=uuid.uuid4())
                user_cart.update(order_status_id=OrderStatusEnum.DELIVERY_COMPLETED.value)

            return JsonResponse({'message' : 'ORDER_COMPLETED'}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
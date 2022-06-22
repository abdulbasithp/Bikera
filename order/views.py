from datetime import date
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from cart.models import CartItem, Cart
from cart.context_processors import counter
from order.models import Order, OrderProduct, Payment
from cart.models import Address
from cart.views import _cart_id
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
from store.models import Product

razorpay_client = razorpay.Client(
    auth=(settings.RAZ_KEY_ID, settings.RAZ_KEY_SECRET))


def place_order(request, total=0, quantity=0):
    
    
    tax_amount = 0
    sub_total = 0
    current_user = request.user
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax_amount = round(float(total) * float(18 / 100), 2)
    sub_total = round(float(total) + tax_amount, 2)
    
    if cart_items.count() <= 0 :
        return redirect('cart:cart')

    if request.method == 'POST':
        address_id = request.POST['address']
        address = Address.objects.get(id=address_id)
        payment_mode = request.POST['payment_method']

        # order object 
        data = Order()
        data.address = address
        data.user = current_user
        data.order_total = sub_total
        data.tax = tax_amount
        data.save()

        # order number 
        today = date.today()

        yr = int(today.strftime('%Y'))
        dt = int(today.strftime('%d'))
        mt = int(today.strftime('%m'))
        d = date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(data.id)

        data.order_number = order_number
        data.save()
        # order completed 

        # creating payment object
        pdata = Payment()
        pdata.user = current_user
        pdata.amount_paid = sub_total
        # if cod choosen 
        if payment_mode == 'cod':
            pdata.payment_id = f'COD{order_number}'
            pdata.payment_method = payment_mode
            pdata.save()

            payment_now = Payment.objects.get(payment_id=pdata.payment_id)
            data.payment = payment_now
            data.is_ordered = True
            data.save()

            for item in cart_items:
                order_product = OrderProduct()
                order_product.order = data
                order_product.payment = payment_now
                order_product.user = request.user
                order_product.product = item.product
                order_product.product_price = item.product.price
                order_product.quantity = item.quantity
                order_product.save()
            
            order = Order.objects.get(order_number=order_number)
            ordered_products = OrderProduct.objects.filter(order = order)
            for ordered_product in ordered_products:
                print(ordered_product.product.title)   
            cart_items.delete()
            context = {
                'order_number': order_number,
                'address': address,
                'tax_amount': tax_amount,
                'sub_total': sub_total,
                'ordered_products': ordered_products,

            }
            return render(request, 'store/order/cod.html', context)

        # if razorpay choosen 
        elif payment_mode == 'razorpay':

            currency = 'INR'
            amount = int(sub_total*100)
            razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
            razorpay_order_id = razorpay_order['id']
            callback_url = 'paymenthandler/'

            context = {}
            context['razorpay_order_id'] = razorpay_order_id
            context['razorpay_merchant_key'] = settings.RAZ_KEY_ID
            context['razorpay_amount'] = amount
            context['currency'] = currency
            context['callback_url'] = callback_url
            

            pdata.payment_id = f'RAZ{order_number}'
            pdata.payment_method = payment_mode
            pdata.save()

            payment_now = Payment.objects.get(payment_id=pdata.payment_id)
            data.payment = payment_now
            data.is_ordered = True
            data.save()

            for item in cart_items:
                order_product = OrderProduct()
                order_product.order = data
                order_product.payment = payment_now
                order_product.user = request.user
                order_product.product = item.product
                order_product.product_price = item.product.price
                order_product.quantity = item.quantity
                order_product.save()

            # cart_items.delete()

            return render(request, 'store/order/payment.html', context)

    else:
        return HttpResponse('error occures!!!')


@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            print(result)
            if request.method == "POST":
              amount = request.POST['productid']
              print(amount)
            if result is None:
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    return HttpResponse('payment success')
                except:
                    return HttpResponse('payment failed')
            else:
                return HttpResponse('result is None')
        except:
            return HttpResponseBadRequest('Exeption occurs')
    else:
        return HttpResponseBadRequest()
 

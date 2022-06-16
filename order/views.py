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

from store.models import Product
from .paytm import generate_checksum, verify_checksum

merchant_key = str(settings.PAYTM_SECRET_KEY)

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

            merchant_key = str(settings.PAYTM_SECRET_KEY)
            print(type(merchant_key))

            param_dict = {
                    'MID': 'CmlnaY36290103763073',
                    'ORDER_ID': str(order_number),
                    'CUST_ID': current_user.id,
                    'TXN_AMOUNT': str(sub_total),
                    'CHANNEL_ID': str(settings.PAYTM_CHANNEL_ID),
                    'WEBSITE': str(settings.PAYTM_WEBSITE),
                    'EMAIL': str(request.user.email),
                        # ('MOBILE_N0', '9911223388'),
                    'INDUSTRY_TYPE_ID': str(settings.PAYTM_INDUSTRY_TYPE_ID),
                    'CALLBACK_URL': 'http://127.0.0.1:8000/order/callback/',

                # ('PAYMENT_MODE_ONLY', 'NO'),
            }
            # print(type(param_dict))
            #
            # param_dict.append(('CHECKSUMHASH',)))
            param_dict['CHECKSUMHASH'] = generate_checksum(param_dict, merchant_key)


            print(param_dict)

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

            return render(request, 'store/order/payment.html', {'param_dict': param_dict})

    else:
        return HttpResponse('error occures!!!')


@csrf_exempt
def callback(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == "CHECKSUMHASH":
            checksum = form[i]
    print(checksum)
    verify = verify_checksum(response_dict,merchant_key,checksum)
    print(verify)
    if verify:
        if response_dict["response"] == '01' :
            print('order successful')
        else:
            print('order unsuccessful')
    HttpResponse('response area ')

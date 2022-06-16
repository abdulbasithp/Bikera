
from decimal import Decimal
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from cart.forms import AddressForm
from store.models import Product
from cart.models import Address, Cart, CartItem
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create( cart_id = _cart_id(request))
        cart.save()
        
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1 ,
            cart = cart 
            )
        cart_item.save()
    return redirect('cart:cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id= product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1 :
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product  = Product.objects.get(id = product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart')
        

def cart(request, total=0, cart_items=None, quantity=0):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except :
        print('cart object does not exist')
        pass
    
    tax_amount = round(float(total) * float(18/100),2)
    sub_total = round(float(total)+tax_amount, 2)
    context = {
        'total':total ,
        'quantity': quantity ,
        'cart_items' : cart_items,
        'tax_amount' : tax_amount ,
        'sub_total' : sub_total ,
    }
    return render(request, 'store/cart/summary.html', context)     


@login_required(login_url='user:login-user')
def checkout(request, total=0, cart_items=None, quantity=0):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        addresses = Address.objects.filter(user=request.user.id)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except :
        print('cart object does not exist')
        pass
    
    tax_amount = round(float(total) * float(18/100),2)
  
    sub_total = round(float(total) + tax_amount, 2)
   
    if request.method == 'POST':
        form = AddressForm(request.POST, )
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
        else:
            messages.error(request,'please give valid credentials.')
    else:
        form = AddressForm()
    context = {
        'form' : form ,
        'total':total ,
        'quantity': quantity ,
        'cart_items' : cart_items,
        'tax_amount' : tax_amount ,
        'sub_total' : sub_total ,
        'addresses' : addresses ,
    }
    return render(request, 'store/cart/checkout.html', context)
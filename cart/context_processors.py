from cart.models import Cart ,CartItem
from .views import _cart_id

def counter(request):
    
    try:
        total_item_qty=0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        total_item_qty = cart_items.count()
            
    except Cart.DoesNotExist:
        total_item_qty = 0
        
    return dict(total_item_qty=total_item_qty)
from wishlist.models import Wishlist ,WishlistItem
from .views import _wishlist_id

def wish_counter(request):
    
    try:
        total_wishitem_qty=0
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
        total_wishitem_qty = wishlist_items.count()
            
    except Wishlist.DoesNotExist:
        total_wishitem_qty = 0
        
    return dict(total_wishitem_qty=total_wishitem_qty)
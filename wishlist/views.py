from django.shortcuts import get_object_or_404, redirect, render

from store.models import Product
from wishlist.models import Wishlist, WishlistItem

# Create your views here.
def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist

def add_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
        print(wishlist)
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create( wishlist_id = _wishlist_id(request))
        wishlist.save()
        
    try:
        wishlist_item = WishlistItem.objects.create(
            user = request.user,
            is_active =True ,
            product = product,
            wishlist = wishlist 
            )
        wishlist_item.save()
    except :
        print('wishlist item create error')
        pass
      
    return redirect('wishlist:wishlist')

def remove_wishlist(request, product_id):
    wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
    product = get_object_or_404(Product, id= product_id)
    wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
    wishlist_item.delete()
    return redirect('cart:cart')

def remove_wishlist_item(request, product_id):
    wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
    product  = Product.objects.get(id = product_id)
    wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
    wishlist_item.delete()
    return redirect('wishlist:wishlist')
        

def wishlist(request, wishlist_items=None,):
    try:
        wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
        print(wishlist)
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist,is_active=True)
        print(wishlist_items)
        for item in wishlist_items:
            print(item.product.title)
    except :
        print('wishlist object does not exist')
        pass
    
    context = {
        'wishlist_items' : wishlist_items, 
    }
    return render(request, 'store/wishlist/summary.html', context)
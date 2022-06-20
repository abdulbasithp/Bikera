from cart.models import Address, Cart, CartItem
from django.shortcuts import redirect, render, get_object_or_404
from order.models import OrderProduct
from store.forms import ProductReviewForm
from wishlist.models import Wishlist, WishlistItem
from .models import Brand, Product, Category, ProductReview
from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from user.models import Account
from order.models import Order
from user.forms import EditProfileForm
import locale
from cart.views import _cart_id
from wishlist.views import _wishlist_id, wishlist
from django.contrib.auth.decorators import login_required


def categories(request):
    return {
        'categories': Category.objects.all()
    }


def brands(request):
    return{
        'brands': Brand.objects.all()
    }


def user_home(request):
    brands = Brand.objects.all()
    context = {
        'brands': brands,
    }
    return render(request, 'store/home.html', context)

#------------- product views -----------------------

def product_review(request,id):
    url= request.META.get('HTTP_REFERER')
     
    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']
        data = ProductReview()
        data.user = request.user
        data.product_id = id
        data.rating = rating
        data.comment = comment
        data.save()
        messages.success(request, 'your review submition is succesful')
        return redirect(url)
    else:
        messages.error(request,'your review is not valid')    
        return redirect(url)
    
def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    # locale.setlocale(locale.LC_MONETARY,'en_US')
    # product_price = locale.currency(product.price, grouping=True)
    product_orders = OrderProduct.objects.filter(user=request.user)
    ordered_product = []
    for product_order in product_orders:
        if product_order.order.shipping_status == 'Delivered':
            ordered_product.append(product_order.product)
    if product in ordered_product:
        can_add_review = True
    else:
        can_add_review = False
    product_reviews = ProductReview.objects.filter(product=product)
  
    context = {
        'product': product,
        'product_price':product.price ,
        'can_add_review': can_add_review,
        'product_reviews':product_reviews ,
    }
    return render(request, 'store/products/detail.html', context)
    
def all_products(request):
    try:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
        print(wishlist_items)
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        print(cart_items)
    except:
        pass
    try:
        products = Product.objects.filter(is_active=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    except:
        messages.error(request, 'Products not found!')
    context = {
        'products': paged_products,
    }
    return render(request, 'store/products/all-product.html', context)





def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_active=True)
    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    return render(request, 'store/products/category.html', {'category': category, 'products': paged_products})


def brandwise_list(request, id):
    brand = Brand.objects.get(id=id)
    products = Product.objects.filter(brand=id)
    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'products': paged_products,
        'brand': brand,
    }
    return render(request, 'store/products/brand-product.html', context)

    #---------------------  search product-------------------


def searched_product(request):
    if request.method == 'POST':
        searched = request.POST['searchField']
        products = Product.objects.filter(title__icontains=searched)
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    
        context = {
            'products': paged_products,
        }
        return render(request, 'store/products/searched-product.html', context)
    else:
        return render(request, 'store/products/searched-product.html', {})

        #------------------ profile---------------------------

@login_required(login_url='user:login-user')
def profile_order(request):

    user = request.user
    order_products = OrderProduct.objects.filter(
        user=user).order_by('-created')

    context = {
        'order_products': order_products,
    }
    return render(request, 'store/profile/orders-list.html', context)


@login_required(login_url='user:login-user')
def profile_detail(request):
    user = request.user
    addresses = Address.objects.filter(user=user)
    
    context = {
        'addresses': addresses,
       
       
    }
    return render(request, 'store/profile/details.html', context)


@login_required(login_url='user:login-user')
def profile_edit(request):
    user = request.user
    form = EditProfileForm(instance=user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST,instance=user)
        if form.is_valid():
            user = form.save(commit=False)      
            user.set_password(user.password)
            user.save()
            return redirect('user:login-user')
    else:
        form = EditProfileForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'store/profile/edit-profile.html', context)



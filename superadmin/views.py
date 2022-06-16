from django.shortcuts import redirect, render
from order.models import Order, Payment
from store.models import Brand, Category, Product
from user.models import Account
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
import locale

from superadmin.forms import ProductForm, BrandAddForm, CategoryAddForm, BlockUserForm


def superadmin_login(request):
    if request.user.is_authenticated:
        return redirect('superadmin:superadmin-home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email = email, password = password)
        print(user)
        if user is not None:
            user = Account.objects.get(email = email)
            if user.is_admin == True :
                login(request,user)
                return redirect('superadmin:superadmin-home')
            else:
                messages.error(request, 'user is not a futac admin')
        else:
            print('user is none')
    return render(request, 'superadmin/login.html')


def superadmin_logout(request):
    logout(request)
    return redirect('superadmin:superadmin-login')

#/////////////////////////dashboard\\\\\\\\\\\\\\\\\\\\\\\
    
@login_required(login_url='superadmin:superadmin-login')
def superadmin_home(request):
    #   customer 
    customers_verified = Account.objects.filter(is_admin=False,is_verified = True)
    customers_unverified = Account.objects.filter(is_admin=False,is_verified = False)
    number_customer = int(customers_verified.count() + customers_unverified.count())
    cdata = [customers_verified.count(),customers_unverified.count()]
    clabel = ['Verified','Unverified']
  
    # orders 
    order_delivered = Order.objects.filter(shipping_status='Delivered')
    order_shipped   = Order.objects.filter(shipping_status='Shipped')
    order_cancelled = Order.objects.filter(shipping_status='Cancelled')
    orders = Order.objects.all()
    number_orders = orders.count()
    odata = [
        order_delivered.count(),
        order_shipped.count(),
        order_cancelled.count(),
        ]
    olabel = ['Deliverd','Shipped','Cancelled']
    
    # total revenue in rupee
    total_revenue = 0
    orders_withoutcancel = Order.objects.exclude(shipping_status='Cancelled')
    for order in orders_withoutcancel:
        total_revenue += order.order_total
    locale.setlocale(locale.LC_MONETARY,'en_IN')
    total_revenue_rupee = locale.currency(total_revenue, grouping=True)
    
    context = {
        'number_customer':number_customer ,
        'cdata':cdata ,
        'clabels':clabel ,
        
        'number_orders': number_orders ,
        'odata': odata ,
        'olabels': olabel ,
        
        'total_revenue_rupee': total_revenue_rupee,
    }
    return render(request, 'superadmin/dashboard.html', context)

#////////////////////////// customer /////////////////////

@login_required(login_url='superadmin:superadmin-login')
def superadmin_customer(request):
    customers = Account.objects.filter(is_admin = False)
    print(customers)  
    return render(request, 'superadmin/customer.html',{'customers': customers})
    

@login_required(login_url='superadmin:superadmin-login')
def customer_detail(request, id):
    customer = Account.objects.get(id=id)
    return render(request, 'superadmin/custom-detail.html', {'customer': customer})


def block_customer(request, id):
    customer = Account.objects.get(id=id)
    if customer.is_active:
        customer.is_active = False
        customer.save()
        print('unblocked')
    else:
        customer.is_active = True
        customer.save()
        print('blocked')
    return redirect('superadmin:superadmin-customer')

#////////////////// product //////////////////////////
 
@login_required(login_url='superadmin:superadmin-login')
def superadmin_product(request):
    products = Product.objects.all()
    return render(request, 'superadmin/product.html', {'products': products})


@login_required(login_url='superadmin:superadmin-login')
def product_detail(request, id):
    product_id = id
    product=Product.objects.get(id = product_id)
    form = ProductForm(instance=product)
   
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            print('form valid')
            form.save()
            return redirect('superadmin:superadmin-product')
        else:
            messages.error(request, 'Form filling is not valid please check it!!')
            print("form not valid")
    else:
        form = ProductForm(instance=product)
    context = {
        'form': form , 
        'product': product,
    }
    return render(request, 'superadmin/prod-detail.html',context)


@login_required(login_url='superadmin:superadmin-login')
def add_product(request):  
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid() :
            print('form is valid')
            form.save()
            return redirect('superadmin:superadmin-product')
        else:
            messages.error(request, 'Form filling is not valid please check it!!')
            print('form is invalid')
    else:
        form = ProductForm()
    context = {
        'form':form
    }
    return render(request, 'superadmin/add-product.html', context)         


def delete_product(request, id):
    product = Product.objects.get(id=id)
    print(product)
    if request.method == "POST":
        product.delete()
        print('deletee success')
        return redirect('superadmin:superadmin-product')
    context = {
        'product':product
    }
    return render(request, 'superadmin/conf-delete-prod.html', context)
    
    #///////////////////// brand//////////////////////////// 
    
def add_brand(request):
    brands = Brand.objects.all()
    if request.method == 'POST':
        form = BrandAddForm(request.POST,request.FILES)
        brand_name = request.POST['name']
        if form.is_valid():
            print('form is valid')
            form.save()
            messages.success(request, 'New brand '+brand_name+' added successfully')
        else:
            print('form is invalid')
    else:
        form = BrandAddForm()
    context = {
        'brands':brands , 
        'form': form ,
    }
    return render(request, 'superadmin/add-brand.html', context)

def delete_brand(request, id):
    brand = Brand.objects.get(id=id)
    brand.delete()
    print(brand.name+'deleted')
    return redirect('superadmin:superadmin-product')

#//////////////////// category ///////////////////

def add_category(request):
    category_list = Category.objects.all()
    if request.method == 'POST':
        form = CategoryAddForm(request.POST)
        category_name = request.POST['name']
        if form.is_valid():
            print('form is valid')
            form.save()
            messages.success(request, 'New Category '+category_name+' added successfully')
        else:
            print('form is invalid')
    else:
        form = CategoryAddForm()
    context = {
        'category_list':category_list ,
        'form':form ,
    }
    return render(request, 'superadmin/add-category.html', context)

def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    print(category.name+'is deleted')
    return redirect('superadmin:superadmin-product')

# ////////////////////////// order ///////////////// 
    
def order_list(request):
    orders = Order.objects.all()
    context = {
        'orders': orders ,
    }
    return render(request, 'superadmin/order/list.html',context)


#/////////////////////////// payments \\\\\\\\\\\\\\\\\\\ 

def payment_list(request):
    payments = Payment.objects.all()
    
    context = {
        'payments': payments ,
        
    }
    return render(request, 'superadmin/payment/list.html', context)
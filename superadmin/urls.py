from django.urls import path
from . import views

app_name = 'superadmin'

urlpatterns = [ 
            path('',views.superadmin_home, name="superadmin-home"),
            path('login/', views.superadmin_login, name="superadmin-login"),
            path('customer/', views.superadmin_customer, name="superadmin-customer"),
            path('product/', views.superadmin_product, name="superadmin-product"),
            path('logout/', views.superadmin_logout, name="superadmin-logout"),
            
            path('customer/detail/<str:id>/', views.customer_detail, name='customer-detail'),
            path('customer/block/<str:id>/', views.block_customer, name="block-customer"),
            
            path('product/detail/<str:id>/', views.product_detail, name='product-detail'),
            path('product/add/', views.add_product, name="add-new-product"),
            path('product/delete/<str:id>/', views.delete_product, name="delete-product"),
            
            path('brand/add/', views.add_brand, name="add-brand"),
            path('brand/delete/<str:id>/', views.delete_brand, name="delete-brand"),
            path('category/add/', views.add_category, name="add-category"),
            path('category/delete/<str:id>/', views.delete_category, name="delete-category"),
            
            path('order/',views.order_list, name="order-list"),
            
            path('payment/', views.payment_list, name='payment-list'),
        ]
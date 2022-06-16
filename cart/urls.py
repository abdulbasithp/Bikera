from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [ 
        
        path('summary/',views.cart, name="cart"),
        path('add_cart/<str:product_id>/', views.add_cart, name="cart-add"),
        path('remove_cart/<str:product_id>/', views.remove_cart, name="remove-cart"),
        path('remove_cart_item/<str:product_id>/', views.remove_cart_item, name="remove-cart-item"),
        
        path('checkout/', views.checkout, name="checkout"),
        ]
from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [ 
        
        path('summary/',views.wishlist, name="wishlist"),
        path('add_wishlist/<str:product_id>/', views.add_wishlist, name="wishlist-add"),
        path('remove_wishlist/<str:product_id>/', views.remove_wishlist, name="remove-wishlist"),
        path('remove_wishlist_item/<str:product_id>/', views.remove_wishlist_item, name="remove-wishlist-item"),
        
        ]
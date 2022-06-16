from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('',views.user_home, name="user-home"),  
    path('products/all/',views.all_products,name="all-products"),
    path('products/<slug:slug>/',views.product_detail, name="product_detail"),
    path('category/<slug:category_slug>/', views.category_list, name="category_list"),
    path('products/brand/<str:id>/', views.brandwise_list, name="brandwise-list"),
    path('search_product/', views.searched_product, name="search-product"),

    path('product/review/<str:id>/',views.product_review, name="product-review"),
    
    path('profile/order/', views.profile_order, name="profile-order"),
    path('profile/detail/', views.profile_detail, name="profile-detail"),
    path('profile/edit/',views.profile_edit, name="profile-edit"),
    
]

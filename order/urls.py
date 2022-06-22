from django.urls import path
from . import views


app_name = 'order'

urlpatterns = [
    path('payment/',views.place_order , name='place-order'),
    path('payment/paymenthandler/', views.paymenthandler, name='paymenthandler'),
]

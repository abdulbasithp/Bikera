from django.contrib import admin
from .models import Address, Cart, CartItem

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Address)
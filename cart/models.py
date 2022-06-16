
from django.db import models
from user.models import Account
from store.models import Product

class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    created_date    = models.DateTimeField(null=True, auto_now_add=True)
    
    def __int__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    is_active=models.BooleanField(default=True) 
    
    
    def get_total(self):
        return self.product.price * self.quantity 
    
    
    def __int__(self):
        return self.product
    
    
    
class Address(models.Model):
    user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    building   = models.CharField(max_length=300)
    street     = models.CharField(max_length=300)
    district   = models.CharField(max_length=50)
    state      = models.CharField(max_length=50)
    pin_code   = models.CharField(max_length=7, null=True)
    mobile     = models.CharField(max_length=10, null=True, unique=True)
    alt_mobile = models.CharField(max_length=10, null=True)
    
    
    def __int__(self):
        return self.first_name
    
    
    
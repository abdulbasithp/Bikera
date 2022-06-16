
from django.db import models
from user.models import Account
from store.models import Product
from cart.models import Address


    

class Payment(models.Model):
   
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    checksum = models.CharField(max_length=500, null=True, blank=True)
    status = models.BooleanField( default=False)
    
    def __str__(self):
        return self.payment_id
    
  

class Order(models.Model):
    SHIPPING_STATUS = (
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),    
    )
    
 
    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True)
    order_number = models.CharField(max_length=20)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    order_note = models.CharField(max_length=200, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    shipping_status = models.CharField(max_length=100, choices=SHIPPING_STATUS, default='Shipped')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.order_number
    
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price  = models.FloatField()
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.order.order_number
    
    
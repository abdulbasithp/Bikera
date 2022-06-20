from django.db import models

# Create your models here.
from user.models import Account
from store.models import Product

class Wishlist(models.Model):
    wishlist_id=models.CharField(max_length=250,blank=True)
    created_date    = models.DateTimeField(null=True, auto_now_add=True)
    
    def __int__(self):
        return self.wishlist_id
    
class WishlistItem(models.Model):
    user = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True) 
    
     
    def __int__(self):
        return self.product
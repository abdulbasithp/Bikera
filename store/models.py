 
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

import user
from user.models import Account



class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    
    class Meta:
        verbose_name_plural = 'categories' 
        
    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    
class Brand(models.Model):
    name    = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='images/logo/', null=True, blank=True)
 

    class Meta:
        verbose_name = "brand"
        verbose_name_plural = "brands"

    def __str__(self):
        return self.name

    

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    brand = models.ForeignKey(Brand, related_name='brand', on_delete=models.CASCADE)
    description = models.TextField(max_length=6000, blank=True)
    
    image1 = models.ImageField(upload_to='images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='images/' , null=True, blank=True)
    image3 = models.ImageField(upload_to='images/', null=True, blank=True)
    image4 = models.ImageField(upload_to='images/', null=True, blank=True)
    
    slug = models.SlugField(max_length=225,blank=True)
    displacement = models.IntegerField(null=True)
    mileage = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(null=True )
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('-created',)
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])
    
    def get_price(self):
        return self.price
    
    
    def __str__(self):
        return self.title
    
    
    
    
class ProductReview(models.Model):
    product = models.ForeignKey(Product,related_name='review', on_delete=models.CASCADE)
    user    = models.ForeignKey(Account, on_delete=models.CASCADE)
    rating  = models.IntegerField(null=True)
    comment = models.TextField(max_length=350,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'ProductReviw'
        verbose_name_plural = 'ProductReviews'
        ordering = ('-created',)
    
    def __str__(self):
        return self.product.title

    

    
    
    
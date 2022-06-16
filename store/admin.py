from django.contrib import admin
from .models import Product, Category, Brand, ProductReview

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','brand','slug','price','stock','created','updated']
    list_filter = ['stock','is_active']
    list_editable = ['price','stock']
    prepopulated_fields = {'slug' : ('title',)}    
    

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name','logo']
    

admin.site.register(ProductReview)
    

    


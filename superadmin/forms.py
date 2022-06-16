from django import forms
from store.models import Product, Brand, Category
from user.models import Account


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category','is_active','brand','image1','image2','image3','image4','title','description','price','stock', 'displacement', 'mileage']
        widgets = {
            'category' : forms.Select(attrs= {'class': "form-select", 'arial-label' : "Default select example"})  ,
            'title' : forms.TextInput(attrs= {'class':"form-control", 'id':"producttitle"}),
            'brand' : forms.Select(attrs= {'class': "form-select", 'arial-label' : "Default select example"})  ,
            'displacement' : forms.TextInput(attrs= {'class':"form-control"}),
            'mileage' : forms.TextInput(attrs= {'class':"form-control"}),
            'description' : forms.Textarea(attrs={'style':'height: 100px ; width : 100%' , 'class': 'form-control mb-3', 'id':'productdesc'}),
            'image1': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'image2': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'image3': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'image4': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class':"form-check-input", 'type':"checkbox", 'role':"switch", 'id':"showtocustomer"}),
        
        }   
        
        
class BrandAddForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name','logo']
        widgets = {
            'name' : forms.TextInput(attrs={'class':"form-control"}),
            'logo': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }
        
        
class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs={'class':"form-control"}),
        }
        
class BlockUserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['is_active']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class':"form-check-input", 'type':"checkbox", 'role':"switch", 'id':"showtocustomer"}),
        }
        
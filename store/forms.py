from django import forms
from store.models import ProductReview

class ProductReviewForm(forms.ModelForm):
    class Meta :
        model = ProductReview
        fields = ['rating','comment']
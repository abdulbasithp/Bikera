from django import forms

from cart.models import Address

class AddressForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput ',
        'placeholder': 'Firstname',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'placeholder': 'Lastname',

    }))
    building = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput ',
        'placeholder': 'building',
    }))
    street = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'placeholder': 'street',

    }))
    district = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput ',
        'placeholder': 'district',
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'placeholder': 'state',

    }))
    pin_code = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'type': 'number',
        'placeholder': 'pin',

    }))
    mobile = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput ',
        'type': 'number',
        'placeholder': 'mobile',
    }))
    alt_mobile = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'id' : 'floatingInput',
        'type': 'number',
        'placeholder': 'alternate mobile',

    }))
    
    class Meta:
        model  = Address
        fields = ['first_name','last_name','building','street','district','pin_code','state','mobile','alt_mobile'] 
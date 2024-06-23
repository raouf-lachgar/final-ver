from django import forms
from .models import custom_user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import piece,car_model,car_serie
from .models import Product

class ProductFilter(forms.ModelForm):
     car_model = forms.ModelChoiceField(queryset=car_model.objects.all(), widget=forms.Select())
     car_serie = forms.ModelChoiceField(queryset=car_serie.objects.all(), widget=forms.Select())
     piece = forms.ModelChoiceField(queryset=piece.objects.all(), widget=forms.Select())
     class Meta:
        
        model = Product
        fields = ['car_model','car_serie','piece']
    
from django import forms
from .models import custom_user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import piece,car_model,car_serie


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = custom_user
        fields = ('username', 'email', 'first_name', 'last_name','phone_num', 'password1', 'password2')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password1', e)
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if custom_user.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")

        return cleaned_data
# forms.py
# users/forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
     car_model = forms.ModelChoiceField(queryset=car_model.objects.all(), widget=forms.Select())
     car_serie = forms.ModelChoiceField(queryset=car_serie.objects.all(), widget=forms.Select())
     piece = forms.ModelChoiceField(queryset=piece.objects.all(), widget=forms.Select())
     class Meta:
        
        model = Product
        fields = ['name', 'car_model','car_serie','piece','price', 'phone_number', 'state', 'city', 'description', 'quantity']
        widgets = {
            'city': forms.Select(),
        }
    
    

from django import forms
from .models import Rating

class RatingForm(forms.Form):
    value = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Rating")

    def clean_value(self):
        value = self.cleaned_data['value']
        try:
            value = int(value)
        except ValueError:
            raise forms.ValidationError("Invalid value: must be an integer.")
        if value < 1 or value > 5:
            raise forms.ValidationError("Invalid value: must be between 1 and 5.")
        return value

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

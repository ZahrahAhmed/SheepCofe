from django import forms
from django.contrib.auth.models import User
from .models import Coffee

class CoffeeForm(forms.ModelForm):
	class Meta:
		model = Coffee
		fields = "__all__"
		exclude = ['user', 'price']

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email', 'password']

        widgets={
        'password': forms.PasswordInput(),
        }

class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
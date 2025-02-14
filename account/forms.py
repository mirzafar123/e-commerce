from django import forms
from .models import Account
from django.contrib.auth.forms import AuthenticationForm , PasswordChangeForm 
from django.contrib.auth import update_session_auth_hash


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Parolingizni kiriting'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Parolni qayta kiriting'
    }))
    user_company = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Kompaniya nomini kiriting'
    }), required=False)  # Majburiy emas qilish
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Parollar bir-biriga mos kelmayapti!")

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email yoki Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Parolingizni kiriting'
    }))
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)
    user_company = forms.CharField(required=False)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'user_company']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),required=False)
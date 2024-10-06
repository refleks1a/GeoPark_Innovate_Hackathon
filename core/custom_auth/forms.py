from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'lq2-form-control lq2-width-100%', 'id': 'input-email',
                                             'placeholder': "email@myemail.com"}),
            'username': forms.TextInput(attrs={'class': 'lq2-form-control lq2-width-100%', 'id': 'input-username',
                                               'placeholder': 'username'}),
        }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class CustomUserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'lq2-form-control lq2-width-100%',
                                                            'id': 'input-email', 'placeholder': "email@myemail.com"}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'lq2-form-control lq2-width-100%',
                                                                 'id': 'input-password', 'placeholder': 'password'}))
    
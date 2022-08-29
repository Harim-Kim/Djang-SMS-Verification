from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User


class UserCreationForm(BaseUserCreationForm):
    phone = forms.CharField(max_length=11, required=True, help_text='Phone number(max 11digits)')

    class Meta:
        model = User
        fields = ('username', 'phone','email', 'password1', 'password2')

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=6, required=True, help_text="문자 인증 번호")
    phone = forms.HiddenInput()
    def set_phone(self, phone):
        self.phone = phone


class reverifyForm(forms.Form):
    phone = forms.CharField(max_length=11, required=True, help_text='Phone number(max 11digits)')

class LoginForm(forms.Form):
    auth_input = forms.CharField(max_length=200)
    password = forms.CharField(max_length=100)

from django.contrib.auth.models import User
from django import forms

from .models import Leave


class LoginForm(forms.ModelForm):

    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'Username'}),)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),)

    class Meta:
        model = User
        exclude = ('last_login', 'is_active', 'date_joined', 'is_staff', 'is_superuser', 'groups', 'user_permissions',
                   'first_name', 'last_name', 'email',)
        fields = ['username', 'password']


class LeaveRequestForm(forms.ModelForm):

    class Meta:
        model = Leave
        fields = ['start_date', 'end_date', 'leave_days']
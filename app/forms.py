from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group, Permission
from django import forms
from .models import CustomGroup 

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class GroupCreationForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = CustomGroup  
        fields = ['name', 'permissions']  

class UnsubscribeFromGroupsForm(forms.Form):
    groups = forms.ModelMultipleChoiceField(
        queryset=CustomGroup.objects.filter(is_active=True),  # Retrieve only active groups
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

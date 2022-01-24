''' Class based forms for 'users' application. '''

from core.widgets import PasswordInput
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdminForm(forms.ModelForm):
    ''' ModelForm class for :model:'users.User'. '''

    class Meta:
        model = User
        widgets = {
            'password': PasswordInput
        }
        fields = '__all__'


class UserSubscriptionAdminForm(forms.ModelForm):
    ''' ModelForm class for user subscription. '''

    class Meta:
        model = User
        fields = '__all__'
        help_texts = {
            'first_name': None,
            'last_name': None,
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Record


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = '__all__'  # This will include all fields from the Record model
        # Alternatively, you can specify only the fields you want to include:
        # fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zipcode')

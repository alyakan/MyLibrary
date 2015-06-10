from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile, Book


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


class BookForm(forms.ModelForm):
    name = forms.CharField()
    author = forms.CharField()

    class Meta:
        model = Book
        exclude = ['slug', 'id']

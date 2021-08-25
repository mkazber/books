from django import forms
from .models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'birth_date', 'avatar')

class BookForm(forms.ModelForm):
    class Meta:
        model = Rating
        widgets = {'user': forms.HiddenInput(), 'book': forms.HiddenInput(), 'date': forms.HiddenInput()}
        exclude = []

class ProfileBooks(forms.ModelForm):
    class Meta:
        model = Profile
        # widgets = {'readBooks': forms.HiddenInput()}
        # fields = ('readBooks')
        exclude = ['user', 'bio', 'birth_date', 'avatar', 'booksToRead']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, label="Pseudonim", required=True)
    email = forms.EmailField(label="Adres Email", required=True)
    subject = forms.CharField(max_length=80, label="Temat wiadomości", required=True)
    message = forms.CharField(widget=forms.Textarea, label="Treść wiadomości", required=True)

class ForgotPassForm(forms.Form):
    email = forms.EmailField(label="Adres Email", required=True)
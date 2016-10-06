from django import forms
from models import *
from django.forms import ModelForm

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = userprofile
        exclude = ('user',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')

class loginForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput())

class searchForm(forms.ModelForm):
	class Meta:
		model = sitevisited
		exclude = ('user',)


		

from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from models import *

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs= \
                {'class':'form-control input-top',
                'name':'username', 
                'placeholder':'Username',
                'autofocus':'true'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs= \
                {'class':'form-control input-bottom',
                'name':'password', 
                'placeholder':'Password'}))


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs= \
                {'class':'form-control input-top',
                'name':'username', 
                'placeholder':'Username',
                'autofocus':'true'}))
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(attrs= \
                {'class':'form-control input-middle',
                'name': 'email', 
                'placeholder':'Email'}))
    password1 = forms.CharField(max_length=200, label='Password', 
                widget = forms.PasswordInput(attrs= \
                {'class':'form-control input-middle',
                'name':'password1', 
                'placeholder':'Password'}))
    password2 = forms.CharField(max_length=200, label='Confirm password',  
                widget = forms.PasswordInput(attrs= \
                {'class':'form-control input-bottom',
                'name':'password2', 
                'placeholder':'Confirm password'}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username


class GrumblForm(forms.Form):
    grumbl = forms.CharField(max_length=42, widget=forms.TextInput(attrs= \
                {'class':'grumbl-text',
                'name':'grumble-text', 
                'placeholder':'Today, what would you like to grumbl?',
                'required':'true'}))

    def clean_grumbl(self):
        # Confirms that the username is not already present in the
        # User model database.
        grumbl = self.cleaned_data.get('grumbl')
        if not grumbl:
            raise forms.ValidationError("Must enter something before grumbling.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return grumbl


class CommentForm(forms.Form):
    grumbl_comment = forms.CharField(max_length=42, widget=forms.TextInput(attrs= \
                {'class':'form-control',
                'placeholder':'Reply to this grumbl...',
                'required':'true'}))
    def clean_grumbl_comment(self):
        # Confirms that the username is not already present in the
        # User model database.
        grumbl_comment = self.cleaned_data.get('grumbl_comment')
        if not grumbl_comment:
            raise forms.ValidationError("Must enter something before commenting.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return grumbl_comment


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('intro', 'location', 'avatar', )    
        widgets = {
            'intro':forms.TextInput(attrs= \
                        {'class':'form-control',
                        'name':'intro', 
                        'placeholder':'Write your brief intro'}), 
            'location':forms.TextInput(attrs= \
                        {'class':'form-control',
                        'name':'location', 
                        'placeholder':'Where are you?'}),
            'avatar':forms.FileInput(attrs= \
                        {'class':'btn btn-lg btn-primary btn-block',
                        'name':'avatar'})
        }

class SearchForm(forms.Form):
    search_content = forms.CharField(max_length=42,
                widget=forms.TextInput(attrs= \
                {'class':'form-control',
                'name':'search-content',
                'placeholder':'Search...'}))
    search_type = forms.ChoiceField(choices= \
                [('search_grumbls','grumbls'), ('search_grumblrs','grumblrs')], 
                widget=forms.RadioSelect( \
                        attrs={'name':"search_type"} \
                ),
                initial = 'search_grumbls')

    def clean_search_content(self):
        # Confirms that the username is not already present in the
        # User model database.
        search_content = self.cleaned_data.get('search_content')
        if not search_content:
            raise forms.ValidationError("Must enter something before searching.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return search_content
        

class ChangePasswordForm(forms.Form):
    password0 = forms.CharField(max_length=200, label='Old password', 
                widget = forms.PasswordInput(attrs= \
                {'class':'form-control',
                'name':'password0', 
                'placeholder':'Old password'}))
    password1 = forms.CharField(max_length=200, label='New password', 
                widget = forms.PasswordInput(attrs= \
                {'class':'form-control',
                'name':'password1', 
                'placeholder':'Password'}))
    password2 = forms.CharField(max_length=200, label='Confirm new password',  
                widget = forms.PasswordInput(attrs= \
                {'class':'form-control',
                'name':'password2', 
                'placeholder':'Confirm password'}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(ChangePasswordForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        password0 = cleaned_data.get('password0')
        if password0 == password1:
            raise forms.ValidationError("New password must be different with old one.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

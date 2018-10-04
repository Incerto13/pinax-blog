from django import forms
from django.contrib.auth.forms import UserCreationForm
from localflavor.us.forms import USStateField, USZipCodeField
from taggit.forms import *

from django.contrib.auth import get_user_model

User = get_user_model()  # this is needs to be here (not model file) due to custom model...


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required. '
                               'Letters, digits and @/./+/-/_ only.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=150, required=True,
                             help_text='Required. Enter valid email address.')
    city = forms.CharField(max_length=50, required=True, help_text='Required.')
    zipcode = USZipCodeField(required=True, help_text='Required.')
    state = USStateField(required=True, help_text='Required.')
    country = forms.CharField(max_length=50, initial="United States",
                              required=True, help_text='Required.')

    class Meta(UserCreationForm):
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'first_name', 'last_name', 'email',
                                                 'city', 'zipcode', 'state', 'password1', 'password2', )


class UpdateProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required.'
                               'Letters, digits and @/./+/-/_ only.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=150, required=True,
                             help_text='Required. Enter valid email address.')
    city = forms.CharField(max_length=50, required=True, help_text='Required.')
    zipcode = USZipCodeField(required=True, help_text='Required.')
    state = USStateField(required=True, help_text='Required.')
    country = forms.CharField(max_length=50, initial="United States",
                              required=True, help_text='Required.')
    bio = forms.CharField(widget=forms.Textarea, required=False)
    birth_date = forms.DateField(required=False)
    organization = forms.CharField(max_length=30, required=False, label='Company / School / Organization')
    image = forms.ImageField(required=False, help_text='Upload/update your profile image.')
    tags = TagField(required=False, label='Skills & Interests', help_text='Separate entries with commas.')


    class Meta:
        model = User
        # all this determines is the order that the fields appear in
        fields = ('username', 'first_name', 'last_name', 'email', 'city', 'zipcode',
                  'state', 'country', 'bio', 'birth_date', 'organization', 'image',)

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email



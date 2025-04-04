import re
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from django.forms import ValidationError, EmailField
from .models import *

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="email",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'autocomplete': 'email'})
    )
    mobile_number = forms.CharField(
        label="",
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number', 'autocomplete': 'tel'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if ' ' in username:
            raise ValidationError(
                'Username cannot contain spaces. Please use only letters, numbers, and symbols like @, _, and -. For example: John_Elder123.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already registered')
        return email

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if User.objects.filter(profile__mobile_number=mobile_number).exists():
            raise ValidationError('Mobile Number already exists')
        if len(mobile_number) < 10:
            raise ValidationError("Mobile number should be at least 10 digits long.")
        if not re.match(r'^\d{10}$', mobile_number):
            raise ValidationError("Mobile number should contain only 10 digits.")
        return mobile_number

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 is None or password2 is None:
            raise ValidationError('Both password fields are required.')
        if len(password1) < 4 or len(password2) < 4:
            raise ValidationError('Password must be at least 4 characters long.')
        if password1 != password2:
            raise ValidationError('Passwords do not match')
        return password2

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'User Name',
            'autocomplete': 'username',
            'id': 'username',
            'style': 'width: 100%,'
        })
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Required. 20 characters or fewer. <span class="text-danger">(No spaces allowed, only letters, numbers, and @/./+/-/_)</span>'
            '</small></span>'
        )
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete': 'new-password',
            'style': 'width: 100%,',
        })
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Your password can\'t be too similar to your other personal information.</li>'
            '<li>Your password must contain at least 8 characters.</li>'
            '<li>Your password can\'t be a commonly used password.</li>'
            '<li>Your password can\'t be entirely numeric.</li>'
            '</ul>'
        )
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = (
            '<span class="form-text text-muted"><small>'
            'Enter the same password as before, for verification.'
            '</small></span>'
        )

class UserInfoForm(forms.ModelForm):
    # Add User model fields
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    profile_picture = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control mt-2', 'id': 'profile-input'})
    )
    mobile_number = forms.CharField(
        label="",
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
        required=True
    )
    address1 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Flat,House no.,Suite,Building,Apartment,Company...'}),
        required=False
    )
    address2 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Area,Street,Landmark...'}),
        required=False
    )
    city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        required=False
    )
    state = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
        required=False
    )
    zipcode = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PINcode'}),
        required=False
    )
    country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ('mobile_number', 'address1', 'address2', 'city', 'state', 'zipcode', 'country',)

    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        # Ensure username and email are populated from the User instance if available
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from users.models import Employee


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'
    }))

    class Meta:
        model = Employee
        fields = ('username', 'password')


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'img_input', 'accept': 'image/*',
        'style': 'position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer;'
    }), required=False)

    class Meta:
        model = Employee
        fields = ('image',)


class AddNewEmployeeForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'phone'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'confirm password'}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'class': 'birthday', 'type': "date"}))

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'username', 'email', 'phone', 'password1', 'password2', 'birthday')

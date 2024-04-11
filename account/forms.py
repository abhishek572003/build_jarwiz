from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model
from .models import *
from django import forms

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(
    max_length=100,
    required = True,
    error_messages = {'required':"Please Enter your email"}
    )
    first_name = forms.CharField(
    max_length=100,
    required = True,
    error_messages = {'required':"Please Enter your name"}
    )
    last_name = forms.CharField(
    max_length=100,
    required = True,
    error_messages = {'required':"Please Enter your last name"}
    )
    username = forms.CharField(
    max_length=200
    )
    phone_num = forms.IntegerField(
        required = True,
        error_messages = {'required':"Please Enter your Password"}
    )
    password1 = forms.CharField(
    required = True,
    error_messages = {'required':"Please Confirm your Password"}
    )
    password2 = forms.CharField(
    required = True,
    error_messages = {'required':"Please Enter your Name"}
    )


    class Meta:

        model = CustomUser
        fields = ['email','phone', 'first_name', 'last_name', 'password1', 'password2']
    
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        email_check = CustomUser.objects.filter(email=email)
        if email_check.exists():
            raise forms.ValidationError('This Email already exists')
        return super(CreateUserForm, self).clean(*args, **kwargs)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class FilesForm(forms.ModelForm):
    file = forms.FileField(widget = forms.TextInput(attrs={
            "name": "files",
            "type": "File",
            "class": "form-control",
            "multiple": "True",
        }), label = "Attach Files to be uploaded")
    class Meta:
        model = FileUpload
        fields = ['file']

class AddPhoneForm(forms.ModelForm):
    phonenum = forms.CharField(widget = forms.TextInput, label= "Enter Additional Phone Number", required=False) 

    class Meta:
        model = UserPhoneNumber
        fields = ['phonenum']

class AddEmailForm(forms.ModelForm):
    email = forms.CharField(widget = forms.TextInput, label= "Enter Additional Email", required=False) 

    class Meta:
        model = UserEmail
        fields = ['email']

class AddTags(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput, label = "Enter Additional Tags Separated by Commas", required = False)

    class Meta:
        model=UploadedDocuments
        fields = ['tags']

class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ['phone_number']


class UserEmailForm(forms.ModelForm):
    class Meta:
        model = EmailAddress
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        }


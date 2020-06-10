from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from accounts.models import AccountUser

class RegistartionForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text = 'Add a valid email address')
    class Meta:
        model = AccountUser
        fields = [
            'email',
            'mobNo',
            'first_name',
            'last_name',
            'aadhaarNo',
            'password1',
            'password2',
        ] 

class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = AccountUser
        fields = ['email', 'password']
    
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Email or Password.')

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = AccountUser
        fields= (
                    'email', 
                    'mobNo',
                    'first_name',
                    'last_name',
                )

    def clean_email(self):
        if self.is_valid:
            email = self.cleaned_data['email']
            try:
                account = AccountUser.objects.exclude(pk=self.instance.pk).get(email=email)
            except AccountUser.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % account.email)
    
    def clean_mobNo(self):
        if self.is_valid:
            mobNo = self.cleaned_data['mobNo']
            try:
                account = AccountUser.objects.exclude(pk=self.instance.pk).get(mobNo=mobNo)
            except AccountUser.DoesNotExist:
                return mobNo
            raise forms.ValidationError('Mobile Number "%s" is already in use.' % account.mobNo)

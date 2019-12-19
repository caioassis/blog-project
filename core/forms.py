from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django import forms

User = get_user_model()


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})


class SignupForm(forms.ModelForm):
    password_confirmation = forms.CharField(label='Password Confirmation', max_length=250,
                                            widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password_confirmation(self):
        password_confirmation = self.cleaned_data.get('password_confirmation')
        password = self.cleaned_data.get('password')
        if password != password_confirmation:
            raise forms.ValidationError("Password and Password Confirmation don't match.")
        return password_confirmation

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }


class AuthorForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

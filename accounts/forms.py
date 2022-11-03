from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Profile
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
        )
        # labels = {
        #     "username": "아이디",
        # }
        def clean_email(self):
            email = self.cleaned_data["email"]
            if len(email) < 3:
                raise ValidationError('너무 짧아요 ㅡㅡ')
            return email


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "first_name",
            "last_name",
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "introduce",
            "nickname",
            "image",
        )

class CheckPasswordForm(forms.Form):
    password = forms.CharField(widget = forms.PasswordInput(), label='')
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password
        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 달라요.')
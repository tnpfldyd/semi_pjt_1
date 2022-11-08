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
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            user = get_user_model().objects.get(username=username)
            if user.secession:
                raise ValidationError('탈퇴일로 부터 1년 동안 재가입은 불가능 합니다. 복구 문의시 고객센터 XXXX-XXXX 로 연락주시기 바랍니다.😢')
            return username
        return username


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
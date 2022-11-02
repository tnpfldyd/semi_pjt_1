from django import forms
from .models import DirectMessage
from django.forms import TextInput

class DirectMessageForm(forms.ModelForm):
    class Meta:
        model = DirectMessage
        fields = ('content',)
        widgets = {
            'content': TextInput(attrs={
                'placeholder': '보낼 메세지를 입력하세요',
            })
        }
        labels = {
            'content': ''
        }
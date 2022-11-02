from django import forms
from .models import DirectMessage


class DirectMessageForm(forms.ModelForm):
    class Meta:
        model = DirectMessage
        fields = ('content',)
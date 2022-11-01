from django import forms
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin
from .models import DirectMessage


class DirectMessageForm(forms.ModelForm):
    class Meta:
        model = DirectMessage
        fields = ('content',)
        widgets = {
            'content': EmojiPickerTextareaAdmin,
        }
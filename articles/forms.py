from django import forms
from .models import Article, Comment
from django.forms import TextInput
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content', 'image',)
        labels = {
            'title': '제목',
            'content': '내용',
            'image': '이미지 업로드',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': '',
        }
        widgets = {
            'content': TextInput(attrs={
                'placeholder': '댓글 내용을 입력해 주세요.',
            })
        }

class ReCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': '',
        }
        widgets = {
            'content': TextInput(attrs={
                'placeholder': '답글 내용을 입력해 주세요.',
            })
        }
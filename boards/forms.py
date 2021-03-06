from django import forms
from .models import Thread, Comment

class NewThreadForm(forms.ModelForm):
    text = forms.CharField(
        widget = forms.Textarea(
            attrs = {'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length = 4000,
        help_text = 'The max length of the text is 4000.'
    )

    class Meta:
        model = Thread
        fields = ['title', 'text']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
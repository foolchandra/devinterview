from django import forms

from fool.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('article', 'created', 'modified')

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content', ]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['maxlength'] = 140
        self.fields['content'].widget.attrs['rows'] = 3
        self.fields['content'].widget.attrs['placeholder'] = 'Write a comment...'

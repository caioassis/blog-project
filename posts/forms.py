from django import forms

from posts.models import Reply


class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ['name', 'email', 'content']


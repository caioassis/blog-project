from django import forms

from posts.models import Reply, Post


class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'thumbnail': forms.FileInput()
        }

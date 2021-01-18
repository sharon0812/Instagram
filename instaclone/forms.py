from .models import Comment, Post
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude =[]
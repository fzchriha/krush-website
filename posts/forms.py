from django import forms
from .models import Post

# This form is for creating the profile of the crush (name, nickname, content, traits/tags)
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'name',
            'nickname',
            'content',
            'tags',
        ]

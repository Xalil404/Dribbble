from django import forms
from user.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['project_title', 'project_image', 'additional_notes', 'live_link', 'github_link']

from django import forms
from user.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['project_title', 'project_image', 'additional_notes', 'live_link', 'github_link']
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project title'}),
            'additional_notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter project description'}),
            'project_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'live_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter live project link'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter GitHub link'}),
        }


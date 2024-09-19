from django import forms
from .models import Profile
from django_summernote.widgets import SummernoteWidget


class ProfileForm(forms.ModelForm):
    reset_profile_picture = forms.BooleanField(required=False, label="Reset to default profile picture")

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'about']
        widgets = {
            'about': SummernoteWidget(),  # Use SummernoteWidget for the content field
        }

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if self.cleaned_data.get('reset_profile_picture'):
            return 'placeholder'  # Return the CloudinaryField default value
        return picture



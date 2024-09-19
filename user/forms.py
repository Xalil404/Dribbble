from django import forms
from .models import Profile, Work
from django_summernote.widgets import SummernoteWidget


# Edit profile
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


#Upload project to profile
class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['project_title', 'live_link', 'github_link', 'project_image', 'additional_notes']
        widgets = {
            'additional_notes': SummernoteWidget(),  # Use SummernoteWidget for the content field
        }

    def clean(self):
        cleaned_data = super().clean()
        for field in self.fields:
            if not cleaned_data.get(field):
                self.add_error(field, f"{field.replace('_', ' ').capitalize()} is required.")

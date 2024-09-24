from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'receiver']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Type your message here...', 'rows': 4}),
            'receiver': forms.HiddenInput(),  # This will be set in the template
        }


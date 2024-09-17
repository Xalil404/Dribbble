from django.db import models

# Create your models here.

class Contact(models.Model):
    SUBJECT_CHOICES = [
        ('Advertising', 'Advertising'),
        ('General Inquiry', 'General Inquiry'),
        ('Feature Request', 'Feature Request'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"
from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_on')
    search_fields = ('full_name', 'email', 'subject')
    list_filter = ('created_on', 'subject')

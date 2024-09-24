from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'content')  # Update 'recipient' to 'receiver'
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('sender', 'receiver', 'timestamp')
    ordering = ('-timestamp',)

    def has_delete_permission(self, request, obj=None):
        return True


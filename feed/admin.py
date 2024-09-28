from django.contrib import admin
from .models import  PostComment


# Register PostComment with a custom admin display
@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'text', 'created_at')  # Customize fields to display
    list_filter = ('created_at', 'user')  # Add filters for easier navigation
    search_fields = ('text', 'user__username')  # Allow search on content and username
    raw_id_fields = ('post',)  # Helps to look up posts by ID for larger datasets
    ordering = ('-created_at',)  # Order by most recent comments



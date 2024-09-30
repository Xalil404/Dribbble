from django.contrib import admin
from .models import Comment, Work, Post

# To delete project comments
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'work', 'created_on')  # Adjust based on your Comment model fields
    search_fields = ('user__username', 'body')  # Allows searching by name and body
    list_filter = ('work', 'created_on')  # Filters for work and date


# To delete projects
@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'user', 'created_at')  # Customize as needed
    search_fields = ('project_title', 'user__username')  # Add search functionality


# To delete projects
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'user', 'created_at')
    search_fields = ('project_title', 'user__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

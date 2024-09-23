from django.contrib import admin
from .models import Comment, Work

# To delete project comments
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'work', 'created_on')  # Adjust based on your Comment model fields
    search_fields = ('name', 'body')  # Allows searching by name and body
    list_filter = ('work', 'created_on')  # Filters for work and date


# To delete projects
@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'user', 'created_at')  # Customize as needed
    search_fields = ('project_title', 'user__username')  # Add search functionality
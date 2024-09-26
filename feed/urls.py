from django.urls import path
from . import views
from .views import social_feed, create_post

urlpatterns = [
    path('feed/', views.social_feed, name='feed'),
    path('feed/create/', views.create_post, name='create_post'),  # Ensure this line is present
]

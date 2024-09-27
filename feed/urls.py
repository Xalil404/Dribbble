from django.urls import path
from . import views
from .views import social_feed, create_post, post


urlpatterns = [
    path('feed/', views.social_feed, name='feed'),
    path('feed/create/', views.create_post, name='create_post'),  
    path('post/<int:id>/', post, name='post'),
]

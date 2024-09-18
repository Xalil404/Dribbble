from . import views
from django.urls import path
from .views import PostList



urlpatterns = [
    path('blogs/', PostList.as_view(), name='blog-list'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]

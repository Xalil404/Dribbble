from django.urls import path
from . import views


urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
]

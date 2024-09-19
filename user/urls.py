from django.urls import path
from . import views
from .views import upload_work, delete_work


urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('upload-work/', upload_work, name='upload_work'),
    path('delete-work/<int:work_id>/', delete_work, name='delete_work'),
]

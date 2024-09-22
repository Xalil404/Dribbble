from django.urls import path
from . import views
from .views import upload_work, delete_work, edit_work, like_project, remove_like, log_project_view


urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('upload-work/', upload_work, name='upload_work'),
    path('work/edit/<int:pk>/', edit_work, name='edit_work'),
    path('delete-work/<int:work_id>/', delete_work, name='delete_work'),
    path('like/<int:project_id>/', like_project, name='like_project'),
    path('remove_like/<int:like_id>/', remove_like, name='remove_like'), 
    path('view/<int:project_id>/', log_project_view, name='log_project_view'),
]

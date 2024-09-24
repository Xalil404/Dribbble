from django.contrib import admin
from django.urls import path
from . import views
from .views import send_message, message_index, delete_conversation


urlpatterns = [
    path('messages/', message_index, name='inbox'),
    path('profile/<str:username>/send_message/', send_message, name='send_message'),
    path('delete_conversation/<int:user_id>/', delete_conversation, name='delete_conversation'),
]

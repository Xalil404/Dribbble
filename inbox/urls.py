from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
]

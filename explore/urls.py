from django.contrib import admin
from django.urls import path
from . import views
from .views import explore_projects, search_results

urlpatterns = [
    path('explore/', views.explore, name='explore'),  # Original explore view
    path('explore/sort/', explore_projects, name='explore_projects'),  # URL for sorting
    path('search/', search_results, name='search_results'),
]

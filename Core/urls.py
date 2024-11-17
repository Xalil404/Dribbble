"""
URL configuration for Core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .views import handler404
from django.contrib import admin
from django.urls import path, include


# these two import statements are for the xml file to be accessible
from django.http import HttpResponse
from django.conf import settings
import os

# Function to serve sitemap
def serve_sitemap(request):
    with open(os.path.join(settings.BASE_DIR, 'sitemap.xml'), 'r') as file:
        return HttpResponse(file.read(), content_type='application/xml')

# Function to serve robots.txt
def serve_robots(request):
    with open(os.path.join(settings.BASE_DIR, 'robots.txt'), 'r') as file:
        return HttpResponse(file.read(), content_type='text/plain')

# Function to serve ads.txt
def serve_ads(request):
    with open(os.path.join(settings.BASE_DIR, 'ads.txt'), 'r') as file:
        return HttpResponse(file.read(), content_type='text/plain')

urlpatterns = [
    path('adminka/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('summernote/', include('django_summernote.urls')),
    path('', include('inbox.urls')),
    path('', include('feed.urls')),
    path('', include('home.urls')),
    path('', include('explore.urls')),
    path('', include('user.urls')),
    path('', include('contact.urls')),
    path('', include('blog.urls')),
    path('sitemap.xml', serve_sitemap, name='sitemap'),
    path('robots.txt', serve_robots, name='robots'),
    path('ads.txt', serve_ads, name='ads'),
]
handler404 = 'Core.views.handler404'

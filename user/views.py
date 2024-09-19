from django.shortcuts import render, get_object_or_404
from .models import Profile, Work, Post, Like
from django.contrib.auth.models import User

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    works = Work.objects.filter(user=user)
    posts = Post.objects.filter(user=user)
    liked_works = Like.objects.filter(user=user, work__isnull=False).select_related('work')
    liked_posts = Like.objects.filter(user=user, post__isnull=False).select_related('post')
    
    context = {
        'profile': profile,
        'works': works,
        'posts': posts,
        'liked_works': liked_works,
        'liked_posts': liked_posts,
    }
    
    return render(request, 'user/profile.html', context)

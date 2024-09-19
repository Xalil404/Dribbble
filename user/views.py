from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Work, Post, Like
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


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


@login_required
def update_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            if form.cleaned_data.get('reset_profile_picture'):
                profile.profile_picture = 'https://res.cloudinary.com/dnbbm9vzi/image/upload/v1726685042/Group_949_oufsqq.png'
            profile.save()
            return redirect('profile', username=request.user.username)  # Redirect after saving
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'user/profile.html', {'form': form})


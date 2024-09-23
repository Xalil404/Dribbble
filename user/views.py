from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Work, Post, Like, View, Comment
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, WorkForm, CommentForm
from django.urls import reverse

from django.views.generic import UpdateView
from django.urls import reverse_lazy

from django.http import JsonResponse





def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    works = Work.objects.filter(user=user)
    open_modal_id = request.GET.get('open_modal')
    print(f"Request GET: {request.GET}")  # Debugging line
    posts = Post.objects.filter(user=user)
    liked_works = Like.objects.filter(user=user, work__isnull=False).select_related('work')
    liked_posts = Like.objects.filter(user=user, post__isnull=False).select_related('post')
    
    if open_modal_id and open_modal_id.isdigit():
        comments = Comment.objects.filter(work__id=int(open_modal_id))
        print(f"Number of comments fetched: {comments.count()} for project ID: {open_modal_id}")
    else:
        comments = Comment.objects.none()

    works_with_likes = [
        {
            'work': work,
            'number_of_likes': work.liked_works.count(),  # This uses the related name
        }
        for work in works
    ]

    
    context = {
        'profile': profile,
        'works': works,
        'posts': posts,
        'liked_works': liked_works,
        'liked_posts': liked_posts,
        'works_with_likes': works_with_likes,
        'open_modal_id': open_modal_id,
        'comments': comments,
    }
    
    return render(request, 'user/profile.html', context)





#def profile_view(request, username):
#    user = get_object_or_404(User, username=username)
#    profile = Profile.objects.get(user=user)
#    works = Work.objects.filter(user=user)
#    open_modal_id = request.GET.get('open_modal')
#    posts = Post.objects.filter(user=user)
#    liked_works = Like.objects.filter(user=user, work__isnull=False).select_related('work')
#    liked_posts = Like.objects.filter(user=user, post__isnull=False).select_related('post')
#    comments = Comment.objects.all() 
#    works_with_likes = [
#        {
#            'work': work,
#            'number_of_likes': work.liked_works.count(),  # This uses the related name
#        }
#        for work in works
#    ]
#
#    
#    context = {
#        'profile': profile,
#        'works': works,
#        'posts': posts,
#        'liked_works': liked_works,
#        'liked_posts': liked_posts,
#        'works_with_likes': works_with_likes,
#        'open_modal_id': open_modal_id,
#        'comments': comments,
#    }
#    
#    return render(request, 'user/profile.html', context)


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


@login_required
def upload_work(request):
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES)
        if form.is_valid():
            work = form.save(commit=False)
            work.user = request.user
            work.save()
            return redirect(reverse('profile', kwargs={'username': request.user.username}))  # Adjust this line
    else:
        form = WorkForm()
    
    return render(request, 'user/upload_work.html', {'form': form})


@login_required
def delete_work(request, work_id):
    # Use work_id instead of pk
    work = get_object_or_404(Work, pk=work_id, user=request.user)

    if request.method == 'POST':
        work.delete()
        return redirect('profile', username=request.user.username)


@login_required
def edit_work(request, pk):
    work = get_object_or_404(Work, pk=pk, user=request.user)

    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES, instance=work)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)  # Redirect to profile after saving
    else:
        form = WorkForm(instance=work)

    return render(request, 'user/edit_work.html', {'form': form, 'work': work})


@login_required
def like_project(request, project_id):
    if request.user.is_authenticated:
        work = get_object_or_404(Work, id=project_id)
        like, created = Like.objects.get_or_create(user=request.user, work=work)

        if not created:  # User already liked the project, so remove the like
            like.delete()

        # Redirect back to the project or profile page
        return redirect('profile', username=request.user.username)  # Or wherever you want to redirect

    return HttpResponse('User not authenticated', status=401)


@login_required
def remove_like(request, like_id):
    if request.user.is_authenticated:
        like = get_object_or_404(Like, id=like_id, user=request.user)
        like.delete()
        return redirect('profile', username=request.user.username)  # Redirect back to the profile page
    return redirect('login')


#This view answers for project views and project comments
#def log_project_view(request, project_id):
#    print("log_project_view called")
#    work = get_object_or_404(Work, id=project_id)
#    print(f"Viewing project: {work.project_title}, ID: {work.id}")
#
#    # Log the view for authenticated and anonymous users
#    View.objects.create(user=request.user if request.user.is_authenticated else None, work=work)
#
#    if request.user.is_authenticated:
#        print(f"User {request.user.username} viewed the project.")
#    else:
#        print("Anonymous user viewed the project.")
#
#    
#    if request.method == 'POST':
#        name = request.POST.get('name')
#        body = request.POST.get('body')
#        comment = Comment(work=work, name=request.user.username, body=body)
#        comment.save()
#        print(f'Comment submitted: {name}, {body}')  # Debug line
#
#    # Fetch comments to pass them to the modal context
#    comments = Comment.objects.filter(work=work)
#
#    # Redirect to the profile page, include the comments in context if needed
#    return redirect(f'/profile/{work.user.username}/?modal=projectDetailsModal{work.id}')



def log_project_view(request, project_id):
    print("log_project_view called")
    work = get_object_or_404(Work, id=project_id)
    print(f"Viewing project: {work.project_title}, ID: {work.id}")

    # Log the view for authenticated and anonymous users
    View.objects.create(user=request.user if request.user.is_authenticated else None, work=work)

    if request.user.is_authenticated:
        print(f"User {request.user.username} viewed the project.")
    else:
        print("Anonymous user viewed the project.")

    
    if request.method == 'POST':
        
        body = request.POST.get('body')
        comment = Comment(work=work, name=request.user.username, body=body)
        comment.save()
        print(f'Comment submitted by {request.user.username}: {body}') 

    # Fetch comments to pass them to the modal context
    comments = Comment.objects.filter(work=work)

    # Redirect to the profile page, include the comments in context if needed
    return redirect(f'/profile/{work.user.username}/?open_modal={work.id}&modal=projectDetailsModal{work.id}')

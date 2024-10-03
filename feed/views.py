
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from user.models import Work, User, Profile, Post
from .forms import PostForm, PostCommentForm

from .models import PostComment

from django.core.paginator import Paginator


@login_required
def social_feed(request):
    # Fetch the top 4 most liked projects
    top_liked_projects = (
        Work.objects
        .annotate(likes_count=Count('liked_works'))  # Assuming 'liked_works' is the related name
        .order_by('-likes_count')[:12]
    )

    # Fetch the top 4 most viewed projects
    top_viewed_projects = (
        Work.objects
        .annotate(views_count=Count('project_views'))  # Assuming 'project_views' is the related name
        .order_by('-views_count')[:12]
    )

    offset = int(request.GET.get('offset', 0))  # Get the offset (how many posts to skip)
    limit = 20  # Load 20 posts at a time

    # Fetch posts, ordered by the created_at field
    posts = Post.objects.all().order_by('-created_at')[offset:offset + limit]  # Limit the posts based on the offset and limit

    # Calculate next offset
    next_offset = offset + limit

    # Get total posts count to check if more posts exist
    total_posts = Post.objects.count()

    # Get all users (members) excluding the current user
    users = User.objects.exclude(id=request.user.id).order_by('?')[:29]  # Randomly select 29 members

    form = PostForm()

    context = {
        'top_liked_projects': top_liked_projects,
        'top_viewed_projects': top_viewed_projects,
        'users': users,
        'posts': posts,
        'form': form,
        'next_offset': next_offset,
        'has_more': total_posts > next_offset,
    }

    return render(request, 'feed/feed.html', context)



@login_required
def create_post(request):
    print("create_post view accessed") 
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Create a new Post instance but don't save it to the database yet
            post = form.save(commit=False)
            post.user = request.user  # Associate the logged-in user with the post
            post.save()  # Save the post to the database

            print("Post saved:", post)  # Debug line for confirming save

            return redirect('feed')  # Redirect to the feed after successful post creation
        else:
            print("Form errors:", form.errors)  # Debug line for form validation errors

    else:
        form = PostForm()  # Initialize an empty form for GET request

    # Fetch all posts to display on the feed page
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'feed/feed.html', {'posts': posts, 'form': form})


@login_required
def post(request, id):  # Use 'id' instead of 'post_id'
    post = get_object_or_404(Post, id=id)
    # Get comments in reverse order (newest first)
    comments = post.comments.order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                return redirect('post', id=post.id)  # Pass 'id' here to match the view parameter
        else:
            return redirect('account_login')  # Redirect non-logged-in users to login

    else:
        form = PostCommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'feed/post.html', context)




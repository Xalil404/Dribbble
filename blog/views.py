from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blog/blogs.html"
    paginate_by = 7


class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)

        post.number_of_views += 1
        post.save()  # Save the updated view count

        comments = post.comments.order_by("-created_on")
        liked = False
        if request.user.is_authenticated and post.likes.filter(id=request.user.id).exists():
            liked = True

        return render(
            request,
            "blog/blog_post.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "comment_form": CommentForm(),
                "liked": liked
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by("-created_on")  # Fetch all comments without approval filter
        liked = False
        if request.user.is_authenticated and post.likes.filter(id=request.user.id).exists():
            liked = True

        if request.user.is_authenticated:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.email = request.user.email
                comment.name = request.user.username
                comment.save()
                comment_form = CommentForm()
            else:
                comment_form = CommentForm()
        else:
            # Handle case where user is not authenticated
            # Optionally, you could return an error message or redirect to login page
            return redirect('login')  # Adjust 'login' to your actual login URL or view name

        return render(
            request,
            "blog/blog_post.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(View):
    
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('blog_post', args=[slug]))

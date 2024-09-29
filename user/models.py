from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = CloudinaryField('image', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    about = models.TextField(blank=True, null=True)

    # Override the save method to set a default image if none is provided
    def save(self, *args, **kwargs):
        if not self.profile_picture:  # If no profile picture is provided
            self.profile_picture = 'https://res.cloudinary.com/dnbbm9vzi/image/upload/v1726685042/Group_949_oufsqq.png'  # Default Cloudinary URL
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username



class Work(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    project_title = models.CharField(max_length=200, null=True, blank=True)
    live_link = models.URLField(null=True, blank=True)
    github_link = models.URLField(null=True, blank=True)
    project_image = CloudinaryField('image', null=True, blank=True)
    additional_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.project_title or "Untitled Project"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    project_title = models.CharField(max_length=200, null=True, blank=True)  # Consider renaming if it represents something else
    live_link = models.URLField(null=True, blank=True)  # Same as above
    github_link = models.URLField(null=True, blank=True)  # Same as above
    project_image = CloudinaryField('image', null=True, blank=True)
    additional_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.project_title or "Untitled Post"



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_posts", null=True, blank=True)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="liked_works", null=True, blank=True)

    class Meta:
        unique_together = ('user', 'post', 'work')  # Ensure a user can only like a post or work once

    def __str__(self):
        return f"{self.user.username} liked {self.post.title if self.post else self.work.project_title}"


class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null for anonymous users
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="project_views")
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} viewed {self.work.project_title}"


class Comment(models.Model):
    work = models.ForeignKey(Work, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.work.project_title}"


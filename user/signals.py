from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(f"Creating profile for user: {instance.username}")
        Profile.objects.create(
            user=instance,
            profile_picture='https://res.cloudinary.com/dnbbm9vzi/image/upload/v1726685042/Group_949_oufsqq.png'  # Set the default profile picture here
        )
        



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Handle cases where profile doesn't exist
        pass

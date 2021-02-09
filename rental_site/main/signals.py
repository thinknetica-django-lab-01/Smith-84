from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import *


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile.objects.create(user=instance)
        user_profile.save()


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    common_users, _ = Group.objects.get_or_create(name="common_users")
    instance.groups.add(common_users)
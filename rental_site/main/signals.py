from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Subscribers, Profile, Ad
from .utils import get_message_body
from .task import send_mail_new_users, send_subscribers_new_ads
from .utils import disable_for_loaddata


@receiver(post_save, sender=User)
@disable_for_loaddata
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile.objects.create(user=instance)
        user_profile.save()


@receiver(post_save, sender=User)
@disable_for_loaddata
def add_user_to_group(sender, instance, created, **kwargs):
    common_users, _ = Group.objects.get_or_create(name="common_users")
    instance.groups.add(common_users)


@receiver(post_save, sender=User)
@disable_for_loaddata
def send_mail_new_user(sender, instance, created, **kwargs):
    """Welcome сообщение."""

    if created:
        send_mail_new_users.delay(email=instance.email)


@receiver(post_save, sender=Ad)
@disable_for_loaddata
def send_subscribers_new_ad(sender, instance, created, **kwargs):
    """Рассылка новых объявлений сразу при добавлении на сайт."""

    if created:
        subscribers = list(Subscribers.objects.all().values_list('email', flat=True))
        message_body = get_message_body(ads=[instance])
        send_subscribers_new_ads.delay(subscribers=subscribers, message=message_body)

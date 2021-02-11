from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import *
from django.core.mail import send_mail, EmailMessage, get_connection
from django.template.loader import render_to_string


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile.objects.create(user=instance)
        user_profile.save()


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    common_users, _ = Group.objects.get_or_create(name="common_users")
    instance.groups.add(common_users)


@receiver(post_save, sender=User)
def send_mail_new_user(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Welcome',
            'Here is the message.',
            'admin@example.com',
            [instance.email],
            fail_silently=False,
        )


@receiver(post_save, sender=Ad)
def send_subscribers_new_ad(sender, instance, created, **kwargs):
    if created:
        subscribers = Subscribers.objects.all().values_list('email', flat=True)
        context = {
            'url': instance.get_full_absolute_url(),
            'realty_type': instance.content_type.name,
            'region': instance.region.name
        }
        message_body = render_to_string(template_name='subscribe/subscribe_email.html', context=context)
        with get_connection() as connection:
            for subscriber in subscribers:
                email = EmailMessage(subject='Новое объявление',
                                     from_email='admin@example.com',
                                     body=message_body, to=[subscriber],
                                     connection=connection)
                email.content_subtype = "html"
                email.send()

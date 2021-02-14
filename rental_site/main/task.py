import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from .models import *
from django.core.mail import send_mail, EmailMessage, get_connection
from rental_site.celery import app
from .utils import get_message_body


def send_subscribers_new_ad():
    """
        Рассылка новых объявлений за неделю
    """
    to_date = datetime.datetime.now()
    from_date = to_date - datetime.timedelta(7)
    subscribers = Subscribers.objects.all().values_list('email', flat=True)
    ads_week = Ad.objects.filter(date_added__range=(from_date, to_date))
    message_body = get_message_body(ads=ads_week)
    with get_connection() as connection:
        for subscriber in subscribers:
            email = EmailMessage(subject='Новое объявления',
                                 from_email='admin@example.com',
                                 body=message_body, to=[subscriber],
                                 connection=connection)
            email.content_subtype = "html"
            email.send()


def start():
    """
        Планировщик рассылки сообщений за неделю
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=send_subscribers_new_ad, trigger='cron', day_of_week='mon', hour='0')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


@app.task
def send_mail_new_users(email):
    send_mail(
        'Welcome',
        'Here is the message.',
        'admin@example.com',
        [email],
        fail_silently=False,
    )
    print('Отправил Welcome письмо', email)


@app.task
def send_subscribers_new_ads(subscribers, message):
    with get_connection() as connection:
        for subscriber in subscribers:
            email = EmailMessage(subject='Новое объявление',
                                 from_email='admin@example.com',
                                 body=message,
                                 to=[subscriber],
                                 connection=connection)
            email.content_subtype = "html"
            email.send()
            print('Отправил письмо', subscriber)

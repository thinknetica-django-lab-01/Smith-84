from django.core.mail import send_mail, EmailMessage, get_connection
from django.template.loader import render_to_string
from .models import Subscribers, Ad
from apscheduler.schedulers.background import BackgroundScheduler
import datetime



def get_message_body(ad_week):
    return render_to_string(template_name='subscribe/subscribe_email.html', context=ad_week)


def send_subscribers_new_ad():
    from_date = datetime.datetime.now()
    to_date = from_date - datetime.timedelta(7)
    subscribers = Subscribers.objects.all().values_list('email', flat=True)

    ad_week = Ad.objects.filter(created_at__range=(from_date, to_date))
    ad_week = Ad.objects.all()

    print(dir(ad_week))

    # message_body = get_message_body(ad_week)
    #
    # with get_connection() as connection:
    #     for subscriber in subscribers:
    #         email = EmailMessage(subject='Новое объявления',
    #                              from_email='admin@example.com',
    #                              body=message_body, to=[subscriber],
    #                              connection=connection)
    #         email.content_subtype = "html"
    #         email.send()


def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(func=send_subscribers_new_ad, trigger='cron', day_of_week='mon', hour='0')
    scheduler.add_job(send_subscribers_new_ad, 'interval', seconds=3)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

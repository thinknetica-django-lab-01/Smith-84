import re
from django.template.loader import render_to_string
from functools import wraps


def check_mobile_ua(request):
    """Возвращает True если request мобильного девайса."""

    mobile_agent_re = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)
    if mobile_agent_re.match(request.META['HTTP_USER_AGENT']):
        return True

    return False


def get_message_body(ads):
    """Генерирует и возращает шаблон email сообщения."""

    return render_to_string(template_name='components/subscribe/subscribe_email.html', context={'ads': ads})


def disable_for_loaddata(signal_handler):
    """Декоратор выключает сигнал при загрузки fixture."""

    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs['raw']:
            return
        signal_handler(*args, **kwargs)
    return wrapper
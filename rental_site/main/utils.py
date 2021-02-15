from django.template.loader import render_to_string


def get_message_body(ads):
    """
        Генерирует и возращает шаблон email сообщения
    """
    return render_to_string(template_name='subscribe/subscribe_email.html', context={'ads': ads})

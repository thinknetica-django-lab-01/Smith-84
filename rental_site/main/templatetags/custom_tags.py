import datetime
from django import template


register = template.Library()


@register.simple_tag
def current_time():
    return datetime.datetime.now()


@register.filter()
def turn_over(value):
    return value[::-1]

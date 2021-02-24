import datetime
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def current_time():
    return datetime.datetime.now()


@register.simple_tag
def ads_options(*args, **kwargs):
    if str(args[0].content_object) == 'Квартира':
        return mark_safe(f'<li>Жилая: {args[0].content_object.living_square}</li>'
                         f'<li>Кухня: {args[0].content_object.kitchen_square}</li>'
                         f'<li>Этаж: {args[0].content_object.floor}</li>')


@register.simple_tag
def ads_title(*args, **kwargs):
    if str(args[0].content_object) == 'Квартира':
        return mark_safe(f'{args[0].content_object.number_of_rooms} комнатная,')


@register.simple_tag
def url_replace(request, field, value):
    query_string = request.GET.copy()
    query_string[field] = value
    return query_string.urlencode()

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter(name='format_currency')
def format_currency(amount):
    formatted_amount = '${0}'.format(intcomma(amount))
    return formatted_amount


@register.filter(name='format_percent')
def format_percent(percent):
    formatted_percent = '{0}%'.format(round(percent, 2))
    return formatted_percent



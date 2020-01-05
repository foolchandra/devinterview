from datetime import datetime
import math

from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='format_date')
def format_date(date):
    return date.strftime('%B %d, %Y')


@register.filter(name='format_date_time_age')
def format_date_time_age(date):
    return get_date_time_age(date)


def get_date_time_age(input_date_time):
    inputtime = input_date_time.astimezone(timezone.get_default_timezone())
    nowtime = datetime.now().astimezone(timezone.get_default_timezone())
    time_duration = nowtime - inputtime
    time_duration_in_seconds = time_duration.total_seconds()

    if not time_duration_in_seconds or math.isnan(time_duration_in_seconds):
        return ''
    else:
        rounded_seconds = int(round(time_duration_in_seconds))
        time_duration_in_minutes = divmod(time_duration_in_seconds, 60)[0]
        rounded_minutes = int(round(time_duration_in_minutes))
        time_duration_in_hours = divmod(time_duration_in_seconds, 3600)[0]
        rounded_hours = int(round(time_duration_in_hours))
        time_duration_in_days = divmod(time_duration_in_seconds, 86400)[0]
        rounded_days = int(round(time_duration_in_days))
        time_duration_in_weeks = divmod(time_duration_in_seconds, 604800)[0]
        rounded_weeks = int(round(time_duration_in_weeks))
        time_duration_in_years = divmod(time_duration_in_seconds, 31556926)[0]
        rounded_years = int(round(time_duration_in_years))

        if time_duration_in_seconds < 1:
            formatted_date_time_ago = '1s'
        elif time_duration_in_seconds < 60:
            formatted_date_time_ago = '{0}{1}'.format(rounded_seconds, 's')
        elif time_duration_in_minutes < 60:
            formatted_date_time_ago = '{0}{1}'.format(rounded_minutes, 'm')
        elif time_duration_in_hours < 24:
            formatted_date_time_ago = '{0}{1}'.format(rounded_hours, 'h')
        elif time_duration_in_days < 7:
            formatted_date_time_ago = '{0}{1}'.format(rounded_days, 'd')
        elif time_duration_in_weeks < 52:
            formatted_date_time_ago = '{0}{1}'.format(rounded_weeks, 'w')
        else:
            formatted_date_time_ago = '{0}{1}'.format(rounded_years, 'y')
        return formatted_date_time_ago

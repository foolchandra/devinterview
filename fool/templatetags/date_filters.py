from django import template

register = template.Library()


@register.filter(name='format_article_date')
def format_article_date(date):
    return date.strftime('%B %d, %Y')

from django import template

register = template.Library()


@register.inclusion_tag('fool/article/comments/comments.html')
def show_article_comments(article):
    comments = article.comments.all().order_by('-created')
    return {'comments': comments, 'article_id': article.id}

from django import template

from fool.models import ArticleAuthor

register = template.Library()


@register.filter(name='format_article_authors_list')
def format_article_authors_list(article):
    """
    Sort author list by primary first, then primary key insert order,
    and return comma separated author bylines.
    """
    article_authors = ArticleAuthor.objects.filter(article=article)

    if not article_authors:
        raise Exception('No authors found for article.')

    article_author_list = [(article_author.id, article_author.author, article_author.is_primary_author)
                           for article_author in article_authors
                           ]

    # Sort by primary author (use negated sorting because False=0 and True=1), and then primary key insert order
    article_author_list.sort(key=lambda x: (not x[2], x[0]))

    return ", ".join(article_author[1].byline for article_author in article_author_list)

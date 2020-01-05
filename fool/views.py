import random

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from fool.forms import CommentForm
from fool.models import Article


class HomepageView(TemplateView):
    template_name = 'fool/index.html'
    top_article_tag_slug = '10-promise'
    top_article = None

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)

        self.set_top_article()

        context.update({
            'top_article': self.top_article,
            'secondary_articles': self.get_secondary_articles()
        })

        return context

    def set_top_article(self):
        """
        Retrieves and sets the top article associated with a tag whose slug is top_article_tag_slug
        """
        try:
            self.top_article = (
                Article.objects
                .filter(tags__slug=self.top_article_tag_slug).order_by('pk')
            )[0]
        except IndexError:
            raise Exception('Could not retrieve top article.')

    def get_secondary_articles(self):
        """
        Retrieve a random set of a maximum of 3 articles that do not include the top article.
        Sort the randomly retrieved articles in reverse chronological order.
        """
        if self.top_article:
            secondary_articles_ids_list = list(
                Article.objects
                .exclude(id=self.top_article.id)
                .values_list('pk', flat=True)
            )

            if not secondary_articles_ids_list:
                raise Exception('There are no secondary articles to display.')

            random_article_ids = random.sample(
                secondary_articles_ids_list,
                3 if len(secondary_articles_ids_list) >= 3 else len(secondary_articles_ids_list)
            )

            secondary_articles = Article.objects.filter(pk__in=random_article_ids).order_by('-publish_at')
            return secondary_articles
        else:
            raise Exception('Set top article before retrieving secondary articles.')


class ArticleView(TemplateView):
    template_name = 'fool/article/article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)

        slug = kwargs['article_slug']

        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Exception('Article with slug "{0}" does not exist.'.format(slug))

        context.update({
            'article': article,
            'related_stock_quotes': article.stock_quotes.all(),
        })

        return context


@csrf_exempt
def add_new_article_comment(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)

            try:
                article = Article.objects.get(pk=request.POST.get('article_id'))
            except Article.DoesNotExist:
                raise Exception('Cannot add comment. Article does not exist.')

            new_comment.article = article
            new_comment.save()

            context = {'comments': article.comments.all().order_by('-created')}
            return render(request, 'fool/article/comments/comments.html', context)
        else:
            raise Exception('Error occurred while adding comment.')

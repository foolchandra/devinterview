import random

from django.views.generic.base import TemplateView

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

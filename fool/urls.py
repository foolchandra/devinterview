"""fool URL Configuration"""

from django.conf.urls import url

from fool.views import HomepageView, ArticleView, add_new_article_comment

urlpatterns = [
    url(r'^(?P<category_slug>[\w-]+)/(?P<publish_year>[\d]{4})/(?P<publish_month>[\d]{2})/(?P<publish_day>[\d]{2})/'
        r'(?P<article_slug>[\w-]+)/$',
        ArticleView.as_view(), name='article'),
    url(r'^article/add-comment/', add_new_article_comment, name='add-comment'),
    url(r'^$', HomepageView.as_view(), name='homepage'),
]

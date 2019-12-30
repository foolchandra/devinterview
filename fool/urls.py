"""fool URL Configuration"""

from django.conf.urls import url

from fool.views import HomepageView

urlpatterns = [
    # url(r'^add-spend/(?P<partner_name>[\w-]+)/(?P<medium>[\w-]+)/(?P<category>[\w-]+)/$',
    #     views.add_spend, name='add_spend'),
    url(r'^$', HomepageView.as_view(), name='homepage'),
]

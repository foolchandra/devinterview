from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone


class TimeStampMixin(models.Model):
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Article(TimeStampMixin):
    uuid = models.CharField(max_length=100)
    slug = models.SlugField()
    featured_image = models.URLField()
    promo = models.TextField()
    headline = models.CharField(max_length=200)
    body = models.TextField()

    # Supporting text
    disclosure = models.TextField()
    pitch = models.ForeignKey('Pitch', null=True, on_delete=models.PROTECT)

    # Related fields
    authors = models.ManyToManyField('Author', through='ArticleAuthor')
    stock_quotes = models.ManyToManyField('StockQuote')
    tags = models.ManyToManyField('Tag', through='ArticleTag')
    bureau = models.ForeignKey('Bureau', null=True, on_delete=models.PROTECT)
    category = models.ForeignKey('Category', null=True, on_delete=models.PROTECT)

    # Date-time fields
    publish_at = models.DateTimeField(default=datetime.now)

    def get_url(self):
        url = reverse('article', kwargs={'category_slug': self.category.slug,
                                         'publish_year': self.publish_at.year,
                                         'publish_month': self.publish_at.month,
                                         'publish_day': self.publish_at.day,
                                         'article_slug': self.slug,
                                         })
        return url


class Author(models.Model):
    author_id = models.IntegerField()
    primary = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    byline = models.CharField(max_length=200)

    # Author bio
    short_bio = models.TextField()
    long_bio = models.TextField(null=True)

    # Author image URLs
    small_avatar_url = models.URLField()
    large_avatar_url = models.URLField()


class ArticleAuthor(models.Model):
    article = models.ForeignKey('Article', on_delete=models.PROTECT)
    author = models.ForeignKey('Author', on_delete=models.PROTECT)
    is_primary_author = models.BooleanField(default=False)

    class Meta:
        unique_together = (('article', 'author'),)


class ArticleTag(models.Model):
    article = models.ForeignKey('Article', on_delete=models.PROTECT)
    tag = models.ForeignKey('Tag', on_delete=models.PROTECT)

    class Meta:
        unique_together = (('article', 'tag'),)


class Bureau(models.Model):
    uuid = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)


class Category(models.Model):
    slug = models.CharField(max_length=100)


class StockQuote(models.Model):
    quote_id = models.IntegerField()
    company_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=5)
    exchange_name = models.CharField(max_length=10)
    description = models.CharField(max_length=500)

    # Price fields
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    change_percent = models.DecimalField(max_digits=10, decimal_places=4, null=True)

    def get_change_amount(self):
        return abs(round(self.current_price * (self.change_percent / 100), 2))

    def is_valid(self):
        if self.exchange_name.lower == 'unknown' or self.current_price == 0.00:
            return False
        return True


class Tag(models.Model):
    uuid = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)


class Pitch(models.Model):
    pitch_id = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.text


class Comment(TimeStampMixin):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self):
        return self.text

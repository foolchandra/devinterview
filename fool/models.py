from datetime import datetime

from django.db import models


class Article(models.Model):
    slug = models.SlugField()
    featured_image = models.URLField()
    promo = models.TextField()
    headline = models.CharField(max_length=200)
    body = models.TextField()
    authors = models.ForeignKey('Author', on_delete=models.PROTECT)

    # Related fields
    quotes = models.ForeignKey('Quote', on_delete=models.PROTECT)
    tags = models.ForeignKey('Tag', on_delete=models.PROTECT)
    bureau = models.ForeignKey('Bureau', on_delete=models.PROTECT)

    # Supporting text
    disclosure = models.TextField()
    pitch = models.ForeignKey('Pitch', on_delete=models.PROTECT)

    # Date-time fields
    publish_at = models.DateTimeField(default=datetime.now)
    created = models.DateTimeField(default=datetime.now)  # mix-in
    modified = models.DateTimeField(default=datetime.now)  # mix-in


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    byline = models.CharField(max_length=200)

    # Author bio
    short_bio = models.TextField()
    long_bio = models.TextField()

    # Author image URLs
    small_avatar_url = models.URLField()
    large_avatar_url = models.URLField()


class Bureau(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)


class Quote(models.Model):
    company_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=5)
    description = models.CharField(max_length=500)

    # Price fields
    current_price = models.DecimalField(max_digits=5, decimal_places=2)
    change_percent = models.DecimalField(max_digits=5, decimal_places=4)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)


class Pitch(models.Model):
    text = models.TextField()

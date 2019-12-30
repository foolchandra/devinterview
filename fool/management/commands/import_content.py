import json

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from fool.models import Article, ArticleAuthor, ArticleTag, Author, Bureau, Category, Pitch, StockQuote, Tag


class Command(BaseCommand):
    help = "Import from content.json into the database"

    def handle(self, *args, **kwargs):

        """
        Open stock quotes JSON file for reading and import data into the database.
        Note: the file is a list of JSON entries
        """

        with open('data/quotes_api.json', encoding='utf8') as list_file:
            data = list_file.read()
            stock_quotes_json_list = json.loads(data)

            for json_stock_quote_data in stock_quotes_json_list:
                stock_quote, newly_created = StockQuote.objects.get_or_create(
                    quote_id=json_stock_quote_data['InstrumentId'],
                    company_name=json_stock_quote_data['CompanyName'],
                    symbol=json_stock_quote_data['Symbol'],
                    description=json_stock_quote_data['Description']
                )
                if newly_created:
                    # Stock quote decimal values are rounded to two decimal places when saved
                    stock_quote.current_price = json_stock_quote_data['CurrentPrice']['Amount']
                    stock_quote.change_percent = json_stock_quote_data['Change']['Amount']
                    stock_quote.save()

        # Open content JSON file for reading and import data into the database
        with open('data/content_api.json', encoding='utf8') as json_file:
            data = json.load(json_file)

            for json_article_data in data['results']:

                """
                Create article with root-level JSON data
                """

                new_article, newly_created = Article.objects.get_or_create(
                    uuid=json_article_data['uuid'],
                    headline=json_article_data['headline'],
                    slug=slugify(json_article_data['headline']),
                    body=json_article_data['body'],
                    promo=json_article_data['promo'],
                    disclosure=json_article_data['disclosure'],
                    publish_at=json_article_data['publish_at'],
                    created=json_article_data['created'],
                    modified=json_article_data['modified']
                )

                """
                Get nested JSON data (Foreign Key)
                """

                # Get article featured image
                json_article_images = json_article_data['images']
                for json_article_image in json_article_images:
                    if json_article_image['featured']:
                        new_article.featured_image = json_article_image['url']
                        break

                # Get article pitch
                pitch = json_article_data['pitch']
                new_pitch, newly_created = Pitch.objects.get_or_create(pitch_id=pitch['id'])
                if newly_created:
                    new_pitch.text = pitch['text']
                    new_pitch.save()
                new_article.pitch = new_pitch

                # Get article bureau
                bureau = json_article_data['bureau']
                new_bureau, newly_created = Bureau.objects.get_or_create(uuid=bureau['uuid'])
                if newly_created:
                    new_bureau.name = bureau['name']
                    new_bureau.slug = bureau['slug']
                    new_bureau.save()
                new_article.bureau = new_bureau

                # Get article category (it is named 'collection' in the JSON API)
                category = json_article_data['collection']
                new_category, newly_created = Category.objects.get_or_create(slug=category['slug'])
                if newly_created:
                    new_category.save()
                new_article.category = new_category

                """
                Get nested JSON data (Many to Many)
                """

                # Save article before adding many-to-many fields
                new_article.save()

                # Get article author(s)
                json_article_authors = json_article_data['authors']
                for json_article_author in json_article_authors:
                    new_author, newly_created = Author.objects.get_or_create(
                        author_id=json_article_author['author_id'],
                        first_name=json_article_author['first_name'],
                        last_name=json_article_author['last_name'],
                        byline=json_article_author['byline'],
                        small_avatar_url=json_article_author['small_avatar_url'],
                        large_avatar_url=json_article_author['large_avatar_url']
                    )
                    if newly_created:
                        new_author.primary = json_article_author['primary']
                        new_author.short_bio = json_article_author['short_bio']
                        new_author.long_bio = json_article_author['long_bio']
                        new_author.save()

                    # Add article-author relationship to many-to-many table
                    article_author, newly_created = ArticleAuthor.objects.get_or_create(
                        article_id=new_article.id,
                        author_id=new_author.id,
                        is_primary_author=json_article_author['primary']
                    )

                    if newly_created:
                        article_author.save()

                # Get article tags
                json_article_tags = json_article_data['tags']
                for json_article_tag in json_article_tags:
                    new_tag, newly_created = Tag.objects.get_or_create(
                        uuid=json_article_tag['uuid'],
                        name=json_article_tag['name'],
                        slug=json_article_tag['slug']
                    )
                    if newly_created:
                        new_tag.save()

                    # Add article-tag relationship to many-to-many table
                    article_tag, newly_created = ArticleTag.objects.get_or_create(
                        article_id=new_article.id,
                        tag_id=new_tag.id
                    )
                    if newly_created:
                        article_tag.save()

                """
                Get article stock quotes (JSON entry for stock quotes is `instruments`).
                If stock quote is in the database (populated by quotes_api.json), then add
                the article-stock_quote relationship to many-to-many table.
                """

                json_article_stock_quotes = json_article_data['instruments']
                for json_article_stock_quote in json_article_stock_quotes:
                    try:
                        stock_quote = StockQuote.objects.get(
                            quote_id=json_article_stock_quote['instrument_id']
                        )
                        new_article.stock_quotes.add(stock_quote)
                    except StockQuote.DoesNotExist:
                        pass


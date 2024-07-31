from django.db import models
from django.db.models import QuerySet, Count


class AuthorManager(models.Manager):
    def get_authors_by_article_count(self) -> QuerySet:
        return self.prefetch_related('articles')\
            .annotate(
                articles_count=Count('articles')
            )\
            .order_by(
                '-articles_count',
                'email'
            )

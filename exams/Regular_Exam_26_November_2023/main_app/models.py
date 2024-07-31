from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.choices import ArticleCategoryChoices
from main_app.managers import AuthorManager
from main_app.mixins import ContentMixin, PublishedOnMixin


class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
        ],
    )

    email = models.EmailField(
        unique=True,
    )

    is_banned = models.BooleanField(
        default=False,
    )

    birth_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2005),
        ],
    )

    website = models.URLField(
        null=True,
        blank=True,
    )

    objects = AuthorManager()


class Article(ContentMixin, PublishedOnMixin):
    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(5),
        ],
    )

    category = models.CharField(
        max_length=10,
        choices=ArticleCategoryChoices.choices,
        default=ArticleCategoryChoices.TECHNOLOGY,
    )

    authors = models.ManyToManyField(
        to=Author,
        related_name='articles',
    )


class Review(ContentMixin, PublishedOnMixin):
    rating = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0),
        ],
    )

    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='author_reviews',
    )

    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        related_name='article_reviews',
    )















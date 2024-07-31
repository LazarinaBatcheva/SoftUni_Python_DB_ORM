from django.db import models


class ArticleCategoryChoices(models.TextChoices):
    TECHNOLOGY = 'Technology', 'Technology'
    SCIENCE = 'Science', 'Science'
    EDUCATION = 'Education', 'Education'

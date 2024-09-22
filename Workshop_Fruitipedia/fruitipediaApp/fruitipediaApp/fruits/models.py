from django.core.validators import MinLengthValidator
from django.db import models
from fruitipediaApp.fruits.validators import OnlyLettersValidator


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name


class Fruit(models.Model):
    name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(2),
            OnlyLettersValidator('Fruit name should contain only letters!')
        ],
    )

    image_url = models.URLField(
        null=False,
        blank=False,
    )

    description = models.TextField(
        null=False,
        blank=False,
    )

    nutrition = models.TextField(
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        null=True,
        related_name='fruits',
    )

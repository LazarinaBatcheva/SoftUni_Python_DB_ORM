from django.core.validators import MinLengthValidator
from django.db import models


class ContentMixin(models.Model):
    content = models.TextField(
        validators=[
            MinLengthValidator(10),
        ],
    )

    class Meta:
        abstract = True


class PublishedOnMixin(models.Model):
    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        abstract = True

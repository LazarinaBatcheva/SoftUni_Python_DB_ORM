from django.db import models


class WinsMixin(models.Model):
    wins = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        abstract = True


class ModifiedAtMixin(models.Model):

    modified_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


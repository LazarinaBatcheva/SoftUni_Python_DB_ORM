from django.db import models


class AwardedMixin(models.Model):
    is_awarded = models.BooleanField(
        default=False,
    )

    class Meta:
        abstract = True


class UpdatedMixin(models.Model):
    last_updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True

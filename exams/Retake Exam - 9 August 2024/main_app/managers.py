from django.db import models
from django.db.models import Count, QuerySet


class HouseManager(models.Manager):
    def get_houses_by_dragons_count(self) -> QuerySet:
        return self.prefetch_related('dragons')\
            .annotate(dragons_count=Count('dragons'))\
            .order_by(
                '-dragons_count',
                'name'
            )

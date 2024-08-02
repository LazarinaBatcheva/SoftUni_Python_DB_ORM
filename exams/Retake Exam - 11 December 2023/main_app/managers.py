from django.db import models
from django.db.models import QuerySet, Count


class TennisPlayerManager(models.Manager):
    def get_tennis_players_by_wins_count(self) -> QuerySet:
        return self.prefetch_related('winner_matches')\
            .annotate(
                wins_count=Count('winner_matches')
            )\
            .order_by(
                '-wins_count',
                'full_name'
            )

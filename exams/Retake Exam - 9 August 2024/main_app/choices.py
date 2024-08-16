from django.db import models


class DragonBreathChoices(models.TextChoices):
    FIRE = 'Fire', 'Fire'
    ICE = 'Ice', 'Ice'
    LIGHTNING = 'Lightning', 'Lightning'
    UNKNOWN = 'Unknown', 'Unknown'



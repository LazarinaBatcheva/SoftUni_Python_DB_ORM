from django.db import models


class MissionStatusChoices(models.TextChoices):
    PLANNED = 'Planned', 'Planned'
    ONGOING = 'Ongoing', 'Ongoing'
    COMPLETED = 'Completed', 'Completed'

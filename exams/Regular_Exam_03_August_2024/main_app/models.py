from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator
from django.db import models

from main_app.choices import MissionStatusChoices
from main_app.managers import AstronautManager
from main_app.mixins import LaunchDateMixin


class BaseModel(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2),
        ],
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class Astronaut(BaseModel):
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\d{1,15}$'
            )
        ],
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    spacewalks = models.IntegerField(
        validators=[
            MinValueValidator(0),
        ],
        default=0,
    )

    objects = AstronautManager()


class Spacecraft(BaseModel, LaunchDateMixin):
    manufacturer = models.CharField(
        max_length=100,
    )

    capacity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
        ],
    )

    weight = models.FloatField(
        validators=[
            MinValueValidator(0.0),
        ],
    )


class Mission(BaseModel, LaunchDateMixin):
    description = models.TextField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=9,
        choices=MissionStatusChoices.choices,
        default=MissionStatusChoices.PLANNED,
    )

    spacecraft = models.ForeignKey(
        to=Spacecraft,
        on_delete=models.CASCADE,
        related_name='spacecraft_missions'
    )

    astronauts = models.ManyToManyField(
        to=Astronaut,
        related_name='astronaut_missions'
    )

    commander = models.ForeignKey(
        to=Astronaut,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commander_missions'
    )

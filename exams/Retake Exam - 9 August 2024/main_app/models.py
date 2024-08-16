from datetime import date

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from main_app.choices import DragonBreathChoices
from main_app.managers import HouseManager
from main_app.mixins import WinsMixin, ModifiedAtMixin


class BaseModel(models.Model):
    name = models.CharField(
        max_length=80,
        validators=[
            MinLengthValidator(5),
        ],
        unique=True,
    )

    class Meta:
        abstract = True


class House(BaseModel, WinsMixin, ModifiedAtMixin):
    motto = models.TextField(
        null=True,
        blank=True,
    )

    is_ruling = models.BooleanField(
        default=False,
    )

    castle = models.CharField(
        max_length=80,
        null=True,
        blank=True,
    )

    objects = HouseManager()


class Dragon(BaseModel, WinsMixin, ModifiedAtMixin):
    power = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(10.0),
        ],
        default=1.0,
    )

    breath = models.CharField(
        max_length=9,
        choices=DragonBreathChoices.choices,
        default=DragonBreathChoices.UNKNOWN,
    )

    is_healthy = models.BooleanField(
        default=True,
    )

    birth_date = models.DateField(
        default=date.today,
    )

    house = models.ForeignKey(
        to=House,
        on_delete=models.CASCADE,
        related_name='dragons',
    )


class Quest(BaseModel, ModifiedAtMixin):
    code = models.CharField(
        max_length=4,
        validators=[
            RegexValidator(regex=r'^[A-Za-z#]{4}$'),
        ],
        unique=True,
    )

    reward = models.FloatField(
        default=100.0,
    )

    start_time = models.DateTimeField()

    dragons = models.ManyToManyField(
        to=Dragon,
        related_name='dragons_quests',
    )

    host = models.ForeignKey(
        to=House,
        on_delete=models.CASCADE,
        related_name='host_quests'
    )

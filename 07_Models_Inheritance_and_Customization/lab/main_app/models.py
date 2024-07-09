from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from main_app.choices import ZooKeeperSpecialtyChoices


class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs["choices"] = (
            (True, "Available"),
            (False, "Not Available")
        )

        kwargs["default"] = True

        super().__init__(*args, **kwargs)


class Animal(models.Model):
    name = models.CharField(
        max_length=100,
    )

    species = models.CharField(
        max_length=100,
    )

    birth_date = models.DateField()

    sound = models.CharField(
        max_length=100,
    )

    @property
    def age(self):
        age_in_days = date.today() - self.birth_date
        age = age_in_days.days // 365

        return age


class Mammal(Animal):
    fur_color = models.CharField(
        max_length=50,
    )


class Bird(Animal):
    wing_span = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )


class Reptile(Animal):
    scale_type = models.CharField(
        max_length=50,
    )


class Employee(models.Model):
    first_name = models.CharField(
        max_length=50,
    )

    last_name = models.CharField(
        max_length=50,
    )

    phone_number = models.CharField(
        max_length=10,
    )

    class Meta:
        abstract = True


class ZooKeeper(Employee):
    specialty = models.CharField(
        max_length=10,
        choices=ZooKeeperSpecialtyChoices,
    )

    managed_animals = models.ManyToManyField(
        to=Animal,
    )

    def clean(self):
        if self.specialty not in ZooKeeperSpecialtyChoices:
            raise ValidationError("Specialty must be a valid choice.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Veterinarian(Employee):
    license_number = models.CharField(
        max_length=10,
    )

    availability = BooleanChoiceField()


class ZooDisplayAnimal(Animal):
    ENDANGERED_SPECIES = [
        "Cross River Gorilla",
        "Orangutan",
        "Green Turtle",
    ]

    class Meta:
        proxy = True

    def display_info(self) -> str:
        return (f"Meet {self.name}! "
                f"Species: {self.species}, "
                f"born {self.birth_date}. "
                f"It makes a noise like '{self.sound}'.")

    def is_endangered(self) -> str:
        if self.species in self.ENDANGERED_SPECIES:
            return f"{self.species} is at risk!"
        else:
            return f"{self.species} is not at risk."









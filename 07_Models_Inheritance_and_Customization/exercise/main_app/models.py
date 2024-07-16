from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from main_app.custom_fields import StudentIDField, MaskedCreditCardField


class BaseCharacter(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField()


class Mage(BaseCharacter):
    elemental_power = models.CharField(
        max_length=100,
    )

    spellbook_type = models.CharField(
        max_length=100,
    )


class Assassin(BaseCharacter):
    weapon_type = models.CharField(
        max_length=100,
    )

    assassination_technique = models.CharField(
        max_length=100,
    )


class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(
        max_length=100,
    )

    demon_slaying_ability = models.CharField(
        max_length=100,
    )


class TimeMage(Mage):
    time_magic_mastery = models.CharField(
        max_length=100,
    )

    temporal_shift_ability = models.CharField(
        max_length=100,
    )


class Necromancer(Mage):
    raise_dead_ability = models.CharField(
        max_length=100,
    )


class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(
        max_length=100,
    )

    venomous_bite_ability = models.CharField(
        max_length=100,
    )


class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(
        max_length=100,
    )


class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(
        max_length=100,
    )

    retribution_ability = models.CharField(
        max_length=100,
    )


class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(
        max_length=100,
    )


class UserProfile(models.Model):
    username = models.CharField(
        max_length=70,
        unique=True,
    )

    email = models.EmailField(
        unique=True,
    )

    bio = models.TextField(
        null=True,
        blank=True,
    )


class Message(models.Model):
    sender = models.ForeignKey(
        to=UserProfile,
        related_name="sent_messages",
        on_delete=models.CASCADE,
    )

    receiver = models.ForeignKey(
        to=UserProfile,
        related_name="received_messages",
        on_delete=models.CASCADE,
    )

    content = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    is_read = models.BooleanField(
        default=False,
    )

    def mark_as_read(self) -> None:
        self.is_read = True

    def reply_to_message(self, reply_content: str) -> 'Message':
        message = Message(
            sender=self.receiver,
            receiver=self.sender,
            content=reply_content
        )

        message.save()

        return message

    def forward_message(self, receiver: UserProfile) -> "Message":
        message = Message(
            sender=self.receiver,
            receiver=receiver,
            content=self.content
        )

        message.save()

        return message


class Student(models.Model):
    name = models.CharField(
        max_length=100,
    )

    student_id = StudentIDField()


class CreditCard(models.Model):
    card_owner = models.CharField(
        max_length=100,
    )

    card_number = MaskedCreditCardField()


class Hotel(models.Model):
    name = models.CharField(
        max_length=100,
    )

    address = models.CharField(
        max_length=200,
    )


class Room(models.Model):
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
    )

    number = models.CharField(
        max_length=100,
        unique=True,
    )

    capacity = models.PositiveIntegerField()

    total_guests = models.PositiveIntegerField()

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def clean(self) -> None:
        if self.total_guests > self.capacity:
            raise ValidationError(f"Total guests are more than the capacity of the room")

    def save(self, *args, **kwargs) -> str:
        self.clean()

        super().save(*args, **kwargs)

        return f"Room {self.number} created successfully"


class BaseReservation(models.Model):

    class Meta:
        abstract = True

    room = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE,
    )

    start_date = models.DateField()

    end_date = models.DateField()

    def reservation_period(self) -> int:
        return (self.end_date - self.start_date).days

    def calculate_total_cost(self) -> Decimal:
        total_costs = self.reservation_period() * self.room.price_per_night

        return round(total_costs, 2)

    @property
    def is_available(self) -> bool:
        already_reserved = self.__class__.objects.filter(
            room=self.room,
            end_date__gte=self.start_date,
            start_date__lte=self.end_date
        )

        return not already_reserved.exists()

    def clean(self) -> None:
        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")
        elif not self.is_available:
            raise ValidationError(f"Room {self.room.number} cannot be reserved")


class RegularReservation(BaseReservation):
    def save(self, *args, **kwargs) -> str:
        super().clean()

        super().save(*args, **kwargs)

        return f"Regular reservation for room {self.room.number}"


class SpecialReservation(BaseReservation):
    def save(self, *args, **kwargs) -> str:
        super().clean()

        super().save(*args, **kwargs)

        return f"Special reservation for room {self.room.number}"

    def extend_reservation(self, days: int):
        self.end_date += timedelta(days=days)

        if not self.is_available:
            raise ValidationError("Error during extending reservation")

        self.save()

        return f"Extended reservation for room {self.room.number} with {days} days"

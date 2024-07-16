from typing import Any
from django.core.exceptions import ValidationError
from django.db import models


class StudentIDField(models.PositiveIntegerField):
    def to_python(self, value) -> int or None:
        try:
            return int(value)
        except ValueError:
            raise ValueError("Invalid input for student ID")

    def get_prep_value(self, value) -> Any:
        cleaned_value = self.to_python(value)

        if cleaned_value <= 0:
            raise ValidationError("ID cannot be less than or equal to zero")

        return cleaned_value


class MaskedCreditCardField(models.CharField):
    def __init__(self, *args, **kwargs) -> None:
        kwargs["max_length"] = 20
        super().__init__(*args, **kwargs)

    def to_python(self, value) -> str:
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")
        elif not value.isdigit():
            raise ValidationError("The card number must contain only digits")
        elif len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")

        return f"****-****-****-{value[-4:]}"

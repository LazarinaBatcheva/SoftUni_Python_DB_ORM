from django.core.exceptions import ValidationError


def validate_menu_categories(value):
    for category in ["Appetizers", "Main Course", "Desserts"]:
        if category not in value:
            raise ValidationError(
                'The menu must include each of the categories "Appetizers", "Main Course", "Desserts".'
            )

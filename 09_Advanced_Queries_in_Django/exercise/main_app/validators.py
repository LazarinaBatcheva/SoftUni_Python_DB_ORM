from django.core.exceptions import ValidationError


class RangeValueValidator:
    def __init__(self, min_value: float, max_value: float, message=None):
        self.min_value = min_value
        self.max_value = max_value
        self.message = message

    @property
    def message(self):
        return self.__message
    
    @message.setter
    def message(self, value):
        if value is not None:
            self.__message = value
        else:
            self.__message = f"The rating must be between {self.min_value} and {self.max_value}"

    def __call__(self, value: float):
        if not self.min_value <= value <= self.max_value:
            raise ValidationError(self.message)

    def deconstruct(self):
        return (
            "main_app.validators.RangeValueValidator",  # path
            [self.min_value, self.max_value],   # *args
            {"message": self.message}   # **kwargs
        )

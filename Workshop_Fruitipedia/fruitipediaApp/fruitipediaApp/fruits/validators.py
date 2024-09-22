from django.core.exceptions import ValidationError


class OnlyLettersValidator:
    def __init__(self, message=None):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is not None:
            self.__message = value
        else:
            self.__message = 'The content is incorrect. It should contain only letters!'

    def __call__(self, value:str):
        if not value.isalpha():
            return ValidationError(self.message)

    def deconstruct(self):
        return (
            'fruitipediaApp.fruits.validators.OnlyLettersValidator',
            (),
            {'message': self.message}
        )

from django.db import models


class MealTypeChoice(models.TextChoices):
    BREAKFAST = 'Breakfast', 'Breakfast'
    LUNCH = 'Lunch', 'Lunch'
    DINNER = 'Dinner', 'Dinner'
    SNACK = 'Snack', 'Snack'


class DungeonDifficultyChoice(models.TextChoices):
    EASY = 'Easy', 'Easy'
    MEDIUM = 'Medium', 'Medium'
    HARD = 'Hard', 'Hard'


class WorkoutTypeChoice(models.TextChoices):
    CARDIO = 'Cardio', 'Cardio'
    STRENGTH = 'Strength', 'Strength'
    YOGA = 'Yoga', 'Yoga'
    CROSSFIT = 'CrossFit', 'CrossFit'
    CALISTHENICS = 'Calisthenics', 'Calisthenics'


class LaptopBrandChoice(models.TextChoices):
    ASUS = 'Asus', 'Asus'
    ACER = 'Acer', 'Acer'
    APPLE = 'Apple', 'Apple'
    LENOVO = 'Lenovo', 'Lenovo'
    DELL = 'Dell', 'Dell'


class LaptopOperationSystemChoice(models.TextChoices):
    WINDOWS = 'Windows', 'Windows'
    MAC_OS = 'MacOS', 'MacOS'
    LINUX = 'Linux', 'Linux'
    CHROME_OS = 'Chrome OS', 'Chrome OS'

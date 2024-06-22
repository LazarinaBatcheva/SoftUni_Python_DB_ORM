from django.db import models


class BookGenreChoices(models.TextChoices):
    FICTION = "Fiction", "Fiction"
    NON_FICTION = "Non-Fiction", "Non-Fiction"
    SCIENCE_FICTION = "Science Fiction", "Science Fiction"
    HORROR = "Horror", "Horror"


class Person(models.Model):
    name = models.CharField(
        max_length=30,
    )
    age = models.PositiveIntegerField()


class Blog (models.Model):
    post = models.TextField()
    author = models.CharField(
        max_length=35,
    )


class WeatherForecast(models.Model):
    date = models.DateField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    precipitation = models.FloatField()


class Recipe(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    description = models.TextField()
    ingredients = models.TextField()
    cook_time = models.PositiveIntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class Product(models.Model):
    name = models.CharField(
        max_length=70,
    )
    description = models.TextField()
    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class UserProfile(models.Model):
    username = models.CharField(
        max_length=65,
        unique=True,
    )
    first_name = models.CharField(
        max_length=40,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=40,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        unique=True,
        default="students@softuni.bg",
    )
    bio = models.TextField(
        max_length=120,
    )
    profile_image_url = models.URLField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class Exercise(models.Model):
    name = models.CharField(
        max_length=100,
    )
    description = models.TextField()
    difficulty_level = models.CharField(
        max_length=20,
    )
    duration_minutes = models.PositiveIntegerField()
    equipment = models.CharField(
        max_length=90,
    )
    video_url = models.URLField(
        null=True,
        blank=True,
    )
    calories_burned = models.PositiveIntegerField(
        default=1,
    )
    is_favorite = models.BooleanField(
        default=False,
    )


class Book(models.Model):
    title = models.CharField(
        max_length=30,
    )
    author = models.CharField(
        max_length=100,
    )
    genre = models.CharField(
        max_length=20,
        choices=BookGenreChoices.choices,
    )
    publication_date = models.DateField(
        editable=False,
        auto_now_add=True,
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=8,
    )
    is_available = models.BooleanField(
        default=True,
    )
    rating = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.title

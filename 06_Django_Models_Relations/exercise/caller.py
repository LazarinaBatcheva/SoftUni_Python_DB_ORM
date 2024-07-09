import os
from datetime import date, timedelta

import django
from django.db.models import QuerySet, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Book, Song, Artist, Product, Review, Driver, DrivingLicense, Owner, Car, \
    Registration


def show_all_authors_with_their_books() -> str:
    authors_and_their_books = []

    all_authors = Author.objects.all().order_by('id')

    for author in all_authors:
        authors_books = author.book_set.all()

        if authors_books:
            titles = ', '.join(b.title for b in authors_books)
            authors_and_their_books.append(f'{author.name} has written - {titles}!')

    return '\n'.join(authors_and_their_books)


def delete_all_authors_without_books() -> None:
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name: str) -> QuerySet[Song]:
    artist_songs = Artist.objects.get(name=artist_name).songs.all().order_by('-id')

    return artist_songs


def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str) -> float:
    product = Product.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).get(name=product_name)

    return product.avg_rating


def get_reviews_with_high_ratings(threshold: int) -> QuerySet[Review]:
    searched_reviews = Review.objects.filter(rating__gte=threshold)

    return searched_reviews


def get_products_with_no_reviews() -> QuerySet[Product]:
    product_with_no_reviews = Product.objects.filter(
        reviews__isnull=True
    ).order_by('-name')

    return product_with_no_reviews


def delete_products_without_reviews() -> None:
    get_products_with_no_reviews().delete()


def calculate_licenses_expiration_dates() -> str:
    licenses_expiration_dates = []

    all_licenses = DrivingLicense.objects.all().order_by('-license_number')

    for current_license in all_licenses:
        expiration_date = current_license.issue_date + timedelta(days=365)
        licenses_expiration_dates.append(
            f'License with number: {current_license.license_number} expires on {expiration_date}!'
        )

    return '\n'.join(licenses_expiration_dates)


def get_drivers_with_expired_licenses(due_date: date) -> QuerySet[Driver]:
    expiration_date = due_date - timedelta(days=365)

    drivers_expired_licenses = Driver.objects.filter(
        license__issue_date__gt=expiration_date,
    )

    return drivers_expired_licenses


def register_car_by_owner(owner: Owner) -> str:
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    car.owner = owner
    car.save()

    registration.registration_date = date.today()
    registration.car = car
    registration.save()

    return (f'Successfully registered {car.model} '
            f'to {owner.name} '
            f'with registration number {registration.registration_number}.')


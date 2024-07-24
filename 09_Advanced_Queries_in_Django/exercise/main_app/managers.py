from decimal import Decimal

from django.db import models
from django.db.models import QuerySet, Count, Max, Min, Avg


class RealEstateListingManager(models.Manager):
    def by_property_type(self, property_type: str) -> QuerySet:
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price: Decimal, max_price: Decimal) -> QuerySet:
        return self.filter(price__range=[min_price, max_price])

    def with_bedrooms(self, bedrooms_count: int) -> QuerySet:
        return self.filter(bedrooms=bedrooms_count)

    def popular_locations(self) -> QuerySet:
        return self.values("location")\
            .annotate(location_count=Count("location"))\
            .order_by("-location_count", "location")[:2]


class VideoGameManager(models.Manager):
    def games_by_genre(self, genre: str) -> QuerySet:
        return self.filter(genre=genre)

    def recently_released_games(self, year: int) -> QuerySet:
        return self.filter(release_year__gte=year)

    def highest_rated_game(self) -> QuerySet:
        return self.annotate(highest_rating=Max("rating"))\
            .order_by("-highest_rating")\
            .first()

    def lowest_rated_game(self) -> QuerySet:
        return self.annotate(lowest_rating=Min("rating"))\
            .order_by("lowest_rating")\
            .first()

    def average_rating(self) -> str:
        avr_rating = self.aggregate(average_rating=Avg("rating"))["average_rating"]

        return f"{avr_rating:.1f}"

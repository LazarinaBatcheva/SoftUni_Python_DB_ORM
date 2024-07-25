import os
import django
from django.db.models import Q, Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor, Movie


def get_directors(search_name=None, search_nationality=None) -> str:
    if search_name is None and search_nationality is None:
        return ''

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)
    elif search_name is not None:
        query = query_name
    else:
        query = query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    directors_info = []
    for d in directors:
        directors_info.append(f'Director: {d.full_name}, nationality: {d.nationality}, '
                              f'experience: {d.years_of_experience}')

    return '\n'.join(directors_info)


def get_top_director() -> str:
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ''

    return f'Top Director: {top_director.full_name}, movies: {top_director.movies_count}.'


def get_top_actor() -> str:
    top_actor = Actor.objects.prefetch_related('starring_movies')\
        .annotate(
            movies_count=Count('starring_movies'),
            avg_rating=Avg('starring_movies__rating')
        )\
        .order_by('-movies_count', 'full_name')\
        .first()

    if not top_actor or not top_actor.movies_count:
        return ''

    movies = ', '.join(m.title for m in top_actor.starring_movies.all())

    return (f'Top Actor: {top_actor.full_name}, starring in movies: {movies}, '
            f'movies average rating: {top_actor.avg_rating:.1f}')


def get_actors_by_movies_count() -> str:
    actors = Actor.objects.prefetch_related('actor_movies')\
        .annotate(
            movies_count=Count('actor_movies')
        )\
        .order_by(
            '-movies_count', 'full_name'
        )[:3]

    if not actors or not actors[0].movies_count:
        return ''

    actors_info = []
    for a in actors:
        actors_info.append(f'{a.full_name}, participated in {a.movies_count} movies')

    return '\n'.join(actors_info)


def get_top_rated_awarded_movie() -> str:
    top_movie = Movie.objects\
        .select_related('starring_actor')\
        .prefetch_related('actors')\
        .filter(is_awarded=True)\
        .order_by('-rating', 'title')\
        .first()

    if not top_movie:
        return ''

    starring_actor_full_name = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'
    participating_actors = ', '.join(
        top_movie.actors.order_by('full_name').values_list('full_name', flat=True)
    )

    return (f'Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating}. '
            f'Starring actor: {starring_actor_full_name}. '
            f'Cast: {participating_actors}.')


def increase_rating() -> str:
    movies_to_increase_rating = Movie.objects\
        .filter(is_classic=True, rating__lt=10.0)

    if not movies_to_increase_rating:
        return 'No ratings increased.'

    updated_movies_rating = movies_to_increase_rating.count()

    movies_to_increase_rating.update(rating=F('rating') + 0.1)

    return f'Rating increased for {updated_movies_rating} movies.'

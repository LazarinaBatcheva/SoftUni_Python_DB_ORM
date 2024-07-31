import os
import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Article


def get_authors(search_name=None, search_email=None) -> str:
    if search_name is None and search_email is None:
        return ''

    query = Q()
    if search_name:
        query &= Q(full_name__icontains=search_name)
    if search_email:
        query &= Q(email__icontains=search_email)

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors.exists():
        return ''

    authors_info = []
    for a in authors:
        status = 'Banned' if a.is_banned else 'Not Banned'
        authors_info.append(f'Author: {a.full_name}, email: {a.email}, status: {status}')

    return '\n'.join(authors_info)


def get_top_publisher() -> str:
    top_publisher = Author.objects\
        .get_authors_by_article_count()\
        .filter(articles_count__gt=0)\
        .order_by('-articles_count', 'email')\
        .first()

    if top_publisher is None:
        return ''

    return f'Top Author: {top_publisher.full_name} with {top_publisher.articles_count} published articles.'


def get_top_reviewer() -> str:
    top_reviewer = Author.objects\
        .prefetch_related('author_reviews')\
        .annotate(reviews_count=Count('author_reviews'))\
        .filter(reviews_count__gt=0)\
        .order_by('-reviews_count', 'email')\
        .first()

    if top_reviewer is None:
        return ''

    return f'Top Reviewer: {top_reviewer.full_name} with {top_reviewer.reviews_count} published reviews.'


def get_latest_article() -> str:
    last_article = Article.objects\
        .prefetch_related(
            'authors',
            'article_reviews'
        )\
        .annotate(
            reviews_count=Count('article_reviews'),
            avg_reviews_rating=Avg('article_reviews__rating')
        )\
        .order_by('-published_on')\
        .first()

    if last_article is None:
        return ''

    authors = ', '.join(
        last_article.authors.order_by('full_name').values_list('full_name', flat=True)
    )

    avg_ratting = last_article.avg_reviews_rating or 0.0

    return (f'The latest article is: {last_article.title}. Authors: {authors}. '
            f'Reviewed: {last_article.reviews_count} times. '
            f'Average Rating: {avg_rating:.2f}.')


def get_top_rated_article() -> str:
    top_rated_article = Article.objects \
        .prefetch_related('article_reviews') \
        .annotate(
            reviews_count=Count('article_reviews'),
            avg_reviews_rating=Avg('article_reviews__rating')
        )\
        .filter(reviews_count__gt=0)\
        .order_by(
            '-avg_reviews_rating',
            'title'
        )\
        .first()

    if top_rated_article is None:
        return ''

    avg_rating = top_rated_article.avg_reviews_rating or 0.0

    return (f'The top-rated article is: {top_rated_article.title}, '
            f'with an average rating of {avg_rating:.2f}, '
            f'reviewed {top_rated_article.reviews_count} times.')


def ban_author(email=None) -> str:
    if email is None:
        return 'No authors banned.'

    author_to_ban = Author.objects.filter(email=email).first()

    if not author_to_ban:
        return 'No authors banned.'

    author_to_ban.is_banned = True
    author_to_ban.save()

    reviews_count = author_to_ban.author_reviews.count()
    author_to_ban.author_reviews.all().delete()

    return f'Author: {author_to_ban.full_name} is banned! {reviews_count} reviews deleted.'


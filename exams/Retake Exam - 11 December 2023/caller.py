import os

import django
from django.db.models import Q, Count


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import TennisPlayer, Tournament, Match


def get_tennis_players(search_name=None, search_country=None) -> str:
    if search_name is None and search_country is None:
        return ''

    query = Q()
    if search_name is not None:
        query &= Q(full_name__icontains=search_name)
    if search_country is not None:
        query &= Q(country__icontains=search_country)

    tennis_players = TennisPlayer.objects\
        .filter(query)\
        .order_by('ranking')

    if not tennis_players.exists():
        return ''

    players_info = '\n'.join(
        f'Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}'
        for p in tennis_players
    )

    return players_info


def get_top_tennis_player() -> str:
    top_tennis_player = TennisPlayer.objects\
        .get_tennis_players_by_wins_count()\
        .first()

    if not top_tennis_player:
        return ''

    return f'Top Tennis Player: {top_tennis_player.full_name} with {top_tennis_player.wins_count} wins.'


def get_tennis_player_by_matches_count() -> str:
    the_most_active_tennis_player = TennisPlayer.objects\
        .prefetch_related('tennis_player_matches')\
        .annotate(matches_count=Count('tennis_player_matches'))\
        .filter(matches_count__gt=0)\
        .order_by(
            '-matches_count',
            'ranking'
        )\
        .first()

    if not the_most_active_tennis_player:
        return ''

    return (f'Tennis Player: {the_most_active_tennis_player.full_name} '
            f'with {the_most_active_tennis_player.matches_count} matches played.')


def get_tournaments_by_surface_type(surface=None) -> str:
    if surface is None:
        return ''

    tournaments = Tournament.objects\
        .prefetch_related('tournament_matches')\
        .annotate(matches_count=Count('tournament_matches'))\
        .filter(
            surface_type__icontains=surface,
            # matches_count__gt=0
        )\
        .order_by('-start_date')

    if not tournaments.exists():
        return ''

    tournaments_info = '\n'.join(
        f'Tournament: {t.name}, start date: {t.start_date}, matches: {t.matches_count}'
        for t in tournaments
    )

    return tournaments_info


def get_latest_match_info() -> str:
    latest_match = Match.objects\
        .select_related('tournament', 'winner')\
        .prefetch_related('players')\
        .order_by(
            '-date_played',
            '-id'
        )\
        .first()

    if latest_match is None:
        return ''

    players_names = ' vs '.join(latest_match.players.order_by('full_name').values_list('full_name', flat=True))
    winner = latest_match.winner.full_name if latest_match.winner else 'TBA'

    return (f'Latest match played on: {latest_match.date_played}, '
            f'tournament: {latest_match.tournament.name}, '
            f'score: {latest_match.score}, players: {players_names}, '
            f'winner: {winner}, '
            f'summary: {latest_match.summary}')


def get_matches_by_tournament(tournament_name=None) -> str:
    if tournament_name is None:
        return 'No matches found.'

    matches = Match.objects\
        .select_related('tournament', 'winner')\
        .filter(tournament__name__exact=tournament_name)\
        .order_by('-date_played')

    if not matches.exists():
        return 'No matches found.'

    matches_info = '\n'.join(
        f'Match played on: {m.date_played}, score: {m.score}, winner: {m.winner.full_name if m.winner else "TBA"}'
        for m in matches
    )

    return matches_info

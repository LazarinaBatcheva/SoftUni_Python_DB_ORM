import os
import django
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count, F, Min, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import House, Dragon, Quest


def get_houses(search_string=None) -> str:
    if search_string is None or search_string == '':
        return 'No houses match your search.'

    houses = House.objects\
        .filter(
            Q(name__istartswith=search_string)
            |
            Q(motto__istartswith=search_string)
        )\
        .order_by(
            '-wins',
            'name'
        )

    if not houses.exists():
        return 'No houses match your search.'

    houses_info = '\n'.join(
        f'House: {h.name}, wins: {h.wins}, motto: {h.motto if h.motto else "N/A"}'
        for h in houses
    )

    return houses_info


def get_most_dangerous_house() -> str:
    the_most_dangerous_house = House.objects\
        .get_houses_by_dragons_count()\
        .filter(dragons_count__gt=0)\
        .first()

    if the_most_dangerous_house is None:
        return 'No relevant data.'

    return (f'The most dangerous house is the House of {the_most_dangerous_house.name} '
            f'with {the_most_dangerous_house.dragons_count} dragons. '
            f'Currently {"ruling" if the_most_dangerous_house.is_ruling else "not ruling"} the kingdom.')


def get_most_powerful_dragon() -> str:
    the_most_powerful_dragon = Dragon.objects\
        .select_related('house')\
        .prefetch_related('dragons_quests')\
        .annotate(quests_count=Count('dragons_quests'))\
        .filter(is_healthy=True)\
        .order_by(
            '-power',
            'name'
        )\
        .first()

    if the_most_powerful_dragon is None:
        return 'No relevant data.'

    return (f'The most powerful healthy dragon is {the_most_powerful_dragon.name} '
            f'with a power level of {the_most_powerful_dragon.power}, '
            f'breath type {the_most_powerful_dragon.breath}, '
            f'and {the_most_powerful_dragon.wins} wins, '
            f'coming from the house of {the_most_powerful_dragon.house.name}. '
            f'Currently participating in {the_most_powerful_dragon.quests_count} quests.')


def update_dragons_data() -> str:
    injured_dragons = Dragon.objects\
        .filter(
            is_healthy=False,
            power__gt=1.0
        )

    dragons_affected_count = injured_dragons.count()

    if dragons_affected_count == 0:
        return 'No changes in dragons data.'

    injured_dragons.update(
        power=F('power') - 0.1,
        is_healthy=True
    )

    min_power_level = Dragon.objects\
        .aggregate(min_power=Min('power'))['min_power']

    return (f'The data for {dragons_affected_count} dragon/s has been changed. '
            f'The minimum power level among all dragons is {min_power_level:.1f}')


def get_earliest_quest() -> str:
    earliest_quest = Quest.objects\
        .select_related('host')\
        .prefetch_related('dragons')\
        .annotate(avg_power_level=Avg('dragons__power'))\
        .order_by('start_time')\
        .first()

    if earliest_quest is None:
        return 'No relevant data.'

    dragons_names = '*'.join(earliest_quest.dragons.order_by('-power', 'name').values_list('name', flat=True))

    return (f'The earliest quest is: {earliest_quest.name}, '
            f'code: {earliest_quest.code}, start date: '
            f'{earliest_quest.start_time.day}.{earliest_quest.start_time.month}.{earliest_quest.start_time.year}, '
            f'host: {earliest_quest.host.name}. '
            f'Dragons: {dragons_names}. '
            f'Average dragons power level: {earliest_quest.avg_power_level:.2f}')


def announce_quest_winner(quest_code) -> str:
    try:
        quest_winner = Quest.objects\
            .select_related('host')\
            .prefetch_related('dragons')\
            .get(code__exact=quest_code)
    except ObjectDoesNotExist:
        return 'No such quest.'

    most_powerful_dragon = quest_winner.dragons.order_by('-power', 'name').first()
    most_powerful_dragon.wins = F('wins') + 1
    most_powerful_dragon.save()
    most_powerful_dragon.refresh_from_db()

    dragon_house = most_powerful_dragon.house
    dragon_house.wins = F('wins') + 1
    dragon_house.save()
    dragon_house.refresh_from_db()

    quest_rewards = f'{quest_winner.reward:.2f}'

    quest_winner.delete()

    return (f'The quest: {quest_winner.name} has been won by dragon {most_powerful_dragon.name} '
            f'from house {dragon_house.name}. '
            f'The number of wins has been updated as follows: '
            f'{most_powerful_dragon.wins} total wins for the dragon '
            f'and {dragon_house.wins} total wins for the house. '
            f'The house was awarded with {quest_rewards} coins.')

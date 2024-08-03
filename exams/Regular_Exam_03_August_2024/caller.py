import os
import django
from django.db.models import Q, Count, Sum, F, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Astronaut, Mission, Spacecraft
from main_app.choices import MissionStatusChoices


def get_astronauts(search_string=None) -> str:
    if search_string is None:
        return ''

    astronauts = Astronaut.objects\
        .filter(
            Q(name__icontains=search_string)
            |
            Q(phone_number__icontains=search_string)
        )\
        .order_by('name')

    if not astronauts.exists():
        return ''

    astronauts_info = '\n'.join(
        f'Astronaut: {a.name}, phone number: {a.phone_number}, status: {"Active" if a.is_active else "Inactive"}'
        for a in astronauts
    )

    return astronauts_info


def get_top_astronaut() -> str:
    top_astronaut = Astronaut.objects\
        .get_astronauts_by_missions_count()\
        .filter(missions_count__gt=0)\
        .first()

    if top_astronaut is None:
        return 'No data.'

    return f'Top Astronaut: {top_astronaut.name} with {top_astronaut.missions_count} missions.'


def get_top_commander() -> str:
    top_commander = Astronaut.objects\
        .prefetch_related('commander_missions')\
        .annotate(commanded_missions_count=Count('commander_missions'))\
        .filter(commanded_missions_count__gt=0)\
        .order_by(
            '-commanded_missions_count',
            'phone_number'
        )\
        .first()

    if top_commander is None:
        return 'No data.'

    return f'Top Commander: {top_commander.name} with {top_commander.commanded_missions_count} commanded missions.'


def get_last_completed_mission() -> str:
    last_completed_mission = Mission.objects\
        .select_related('spacecraft', 'commander')\
        .prefetch_related('astronauts')\
        .annotate(total_spacewalks=Sum('astronauts__spacewalks'))\
        .filter(status=MissionStatusChoices.COMPLETED)\
        .order_by('-launch_date')\
        .first()

    if last_completed_mission is None:
        return 'No data.'

    astronauts_names = ', '.join(last_completed_mission.astronauts.order_by('name').values_list('name', flat=True))

    return (f'The last completed mission is: {last_completed_mission.name}. '
            f'Commander: {last_completed_mission.commander.name if last_completed_mission.commander else "TBA"}. '
            f'Astronauts: {astronauts_names}. '
            f'Spacecraft: {last_completed_mission.spacecraft.name}. '
            f'Total spacewalks: {last_completed_mission.total_spacewalks}.')


def get_most_used_spacecraft() -> str:
    the_most_used_spacecraft = Spacecraft.objects\
        .prefetch_related('spacecraft_missions')\
        .annotate(
            missions_count=Count('spacecraft_missions', distinct=True),
            astronauts_count=Count('spacecraft_missions__astronauts', distinct=True)
        )\
        .filter(missions_count__gt=0)\
        .order_by(
            '-missions_count',
            'name'
        )\
        .first()

    if the_most_used_spacecraft is None:
        return 'No data.'

    return (f'The most used spacecraft is: {the_most_used_spacecraft.name}, '
            f'manufactured by {the_most_used_spacecraft.manufacturer}, '
            f'used in {the_most_used_spacecraft.missions_count} missions, '
            f'astronauts on missions: {the_most_used_spacecraft.astronauts_count}.')


def decrease_spacecrafts_weight() -> str:
    spacecrafts_to_update = Spacecraft.objects\
        .prefetch_related('spacecraft_missions')\
        .filter(
            spacecraft_missions__status=MissionStatusChoices.PLANNED,
            weight__gte=200.0
        )\
        .distinct()

    if not spacecrafts_to_update.exists():
        return 'No changes in weight.'

    num_of_spacecrafts_affected = spacecrafts_to_update.count()

    spacecrafts_to_update.update(weight=F('weight') - 200.0)
    avg_weight = Spacecraft.objects\
        .aggregate(avg_weight=Avg('weight'))['avg_weight']

    return (f'The weight of {num_of_spacecrafts_affected} spacecrafts has been decreased. '
            f'The new average weight of all spacecrafts is {avg_weight:.1f}kg')


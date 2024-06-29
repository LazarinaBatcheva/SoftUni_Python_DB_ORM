import os
import django
from django.db.models import QuerySet, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


def create_pet(name: str, species: str) -> str:
    Pet.objects.create(
        name=name,
        species=species,
    )

    return f'{name} is a very cute {species}!'

    # pet = Pet.objects.create(
    #     name=name,
    #     species=species,
    # )
    #
    # return f'{pet.name} is a very cute {pet.species}!'


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical,
    )

    return f'The artifact {name} is {age} years old!'


def rename_artifact(artifact: Artifact, new_name: str) -> None:
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts() -> None:
    Artifact.objects.all().delete()


def show_all_locations() -> str:
    result = []
    all_locations = Location.objects.all().order_by('-id')

    for location in all_locations:
        result.append(f'{location.name} has a population of {location.population}!')

    return '\n'.join(result)


def new_capital() -> None:
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()


def get_capitals() -> QuerySet:
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location() -> None:
    Location.objects.first().delete()


def apply_discount() -> None:
    all_cars = Car.objects.all()

    for car in all_cars:
        percentage_discount = sum(int(n) for n in str(car.year)) / 100
        discount = float(car.price) * percentage_discount
        car.price_with_discount = float(car.price) - discount

    Car.objects.bulk_update(all_cars, ['price_with_discount'])


def get_recent_cars() -> QuerySet:
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car() -> None:
    Car.objects.last().delete()


def show_unfinished_tasks() -> str:
    unfinished_tasks = Task.objects.filter(is_finished=False)

    return '\n'.join(
        f'Task - {task.title} needs to be done until {task.due_date}!'
        for task in unfinished_tasks
    )


def complete_odd_tasks() -> None:
    unfinished_tasks = Task.objects.filter(is_finished=False)

    for task in unfinished_tasks:
        if task.id % 2 != 0:
            task.is_finished = True

    Task.objects.bulk_update(unfinished_tasks, ['is_finished'])


def encode_and_replace(text: str, task_title: str) -> None:
    decoded_text = ''.join((chr(ord(ch) - 3) for ch in text))
    Task.objects.filter(title=task_title).update(description=decoded_text)


def get_deluxe_rooms() -> str:
    all_deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')

    result = [f'Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!'
              for room in all_deluxe_rooms if room.id % 2 == 0]

    return '\n'.join(result)


def increase_room_capacity() -> None:
    all_rooms = HotelRoom.objects.all().order_by('id')

    previous_room_capacity = None

    for room in all_rooms:
        if not room.is_reserved:
            continue

        if previous_room_capacity is None:
            room.capacity += room.id
        else:
            room.capacity += previous_room_capacity

        previous_room_capacity = room.capacity

    HotelRoom.objects.bulk_update(all_rooms, ['capacity'])


def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room() -> None:
    last_room = HotelRoom.objects.last()

    if not last_room.is_reserved:
        last_room.delete()


def update_characters() -> None:
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7
    )

    Character.objects.filter(class_name='Warrior').update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4
    )

    Character.objects.filter(class_name__in=['Assassin', 'Scout']).update(
        inventory='The inventory is empty'
    )


def fuse_characters(first_character: Character, second_character: Character) -> None:
    name = first_character.name + ' ' + second_character.name
    class_name = 'Fusion'
    level = (first_character.level + second_character.level) // 2
    strength = (first_character.strength + second_character.strength) * 1.2
    dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    hit_points = first_character.hit_points + second_character.hit_points

    if first_character.class_name in ['Mage', 'Scout']:
        inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    elif first_character.class_name in ['Warrior', 'Assassin']:
        inventory = 'Dragon Scale Armor, Excalibur'

    Character.objects.create(
        name=name,
        class_name=class_name,
        level=level,
        strength=strength,
        dexterity=dexterity,
        intelligence=intelligence,
        hit_points=hit_points,
        inventory=inventory
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity() -> None:
    Character.objects.update(dexterity=30)


def grand_intelligence() -> None:
    Character.objects.update(intelligence=40)


def grand_strength() -> None:
    Character.objects.update(strength=50)


def delete_characters() -> None:
    Character.objects.filter(inventory='The inventory is empty').delete()


# test code

# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))

# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))

# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)

# print(show_all_locations())

# print(new_capital())

# print(get_capitals())

# apply_discount()

# print(get_recent_cars())

# print(show_unfinished_tasks())

# complete_odd_tasks()

# encode_and_replace("Zdvk#wkh#glvkhv$", "Sample Task")
# print(Task.objects.get(title='Sample Task').description)

# print(get_deluxe_rooms())

# increase_room_capacity()

# reserve_first_room()
# print(HotelRoom.objects.get(room_number=401).is_reserved)

# character1 = Character.objects.create(
#     name='Gandalf',
#     class_name='Mage',
#     level=10,
#     strength=15,
#     dexterity=20,
#     intelligence=25,
#     hit_points=100,
#     inventory='Staff of Magic, Spellbook',
# )
#
# character2 = Character.objects.create(
#     name='Hector',
#     class_name='Warrior',
#     level=12,
#     strength=30,
#     dexterity=15,
#     intelligence=10,
#     hit_points=150,
#     inventory='Sword of Troy, Shield of Protection',
# )
#
# fuse_characters(character1, character2)
# fusion = Character.objects.filter(class_name='Fusion').get()
#
# print(fusion.name)
# print(fusion.class_name)
# print(fusion.level)
# print(fusion.intelligence)
# print(fusion.inventory)

# grand_dexterity()

# grand_intelligence()

# grand_strength()

# delete_characters()

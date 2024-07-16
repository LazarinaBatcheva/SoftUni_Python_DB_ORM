import os
from datetime import date

import django
from django.core.exceptions import ValidationError

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Mage, Necromancer, UserProfile, Message, Student, CreditCard, SpecialReservation, Room, \
    Hotel

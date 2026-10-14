from typing import Any


from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

#import apps
#from apps.movies.models import Movie
#from apps.preferences.models import UserRating
#from apps.rooms.models import Room, Management
from apps.users.models import Friendship, User

class Command(BaseCommand):
    help = "Full in base with demo-data for defence"

    def handle(self, *args, **options):
        # import tmdb catalog -> call_command("import")

        # Creating users


        # FriendShip


        # Rating


        # Rooms 

        self.stdout.write(self.style.SUCCESS("Demo-data ready! Room: DEMO01, password: margo123, nuray123"))
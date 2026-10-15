from django.core.management.base import BaseCommand

from apps.movies.models import Genre, Movie
from apps.preferences.models import TasteProfile, UserRating, WatchlistItem
from apps.rooms.models import Room, RoomMember
from apps.users.models import Friendship, User

USERNAMES = ["Nuray", "Margulan", "Amina"]


DEMO_MOVIES = [
    (1, "Inception", 2000),
    (2, "HarryPotter", 2005),
    (3, "Darkness", 2013),
    (4, "Big Head", 2023),
]


DEMO_RATINGS = {
    "alice": [5.0, 4.5, 3.0, 2.0],
    "bob": [3.5, 5.0, 4.0, 4.5],
    "charlie": [4.0, 2.5, 5.0, 3.5],
}

LETTERBOXD_SCALE = 2 
FAVORITE_GENRE_WEIGHT = 0.8
DEMO_ROOM_CODE = "DEMO01"


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:
        users = self.create_users()
        self.create_friendship(users)
        movies = self.create_movies()
        self.create_preferences(users, movies)
        self.create_room(users)

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo data is ready! Room: {DEMO_ROOM_CODE}, "
                "passwords: Nuray123, Margulan123, Amina123"
            )
        )

    def create_users(self) -> list[User]:
        users = []
        for name in USERNAMES:
            user, _ = User.objects.get_or_create(
                username=name,
                defaults={"email": f"{name}@test.com"},
            )
            user.set_password(f"{name}123")
            user.save()
            users.append(user)
        return users

    def create_friendship(self, users: list[User]) -> None:
        Friendship.objects.get_or_create(
            from_user=users[0],
            to_user=users[1],
            defaults={"status": Friendship.STATUS_ACCEPTED},
        )

    def create_movies(self) -> list[Movie]:
        movies = []
        for tmdb_id, title, year in DEMO_MOVIES:
            movie, _ = Movie.objects.get_or_create(
                tmdb_id=tmdb_id,
                defaults={"title": title, "year": year},
            )
            movies.append(movie)
        return movies

    def create_preferences(self, users: list[User], movies: list[Movie]) -> None:
        genre = Genre.objects.first()

        for user in users:
            stars_list = DEMO_RATINGS.get(user.username)
            if stars_list is None:
                continue

            for movie, stars in zip(movies, stars_list):
                UserRating.objects.get_or_create(
                    user=user,
                    movie=movie,
                    defaults={
                        "raw_rating": stars,
                        "normalized_rating": stars * LETTERBOXD_SCALE,
                        "source": UserRating.SOURCE_LETTERBOXD,
                    },
                )

            WatchlistItem.objects.get_or_create(user=user, movie=movies[-1])

            if genre:
                TasteProfile.objects.get_or_create(
                    user=user,
                    genre=genre,
                    defaults={"weight": FAVORITE_GENRE_WEIGHT},
                )

    def create_room(self, users):
        """Create a demo room and add all users to it."""
        room, created = Room.objects.get_or_create(
            code=DEMO_ROOM_CODE,
            defaults={
                "name": "Demo room",
                "owner": users[0],
                "status": "open",
            },
        )
        for user in users:
            RoomMember.objects.get_or_create(room=room, user=user)
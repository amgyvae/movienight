from django.conf import settings
from django.db.models import (
    CharField, 
    DateField, 
    ForeignKey, 
    FloatField, 
    IntegerField,
    PositiveBigIntegerField,
    FileField,
    TextField, 
    DateTimeField,
    Model,
    UniqueConstraint,
    PROTECT,
    SET_NULL,
)


class Genre(Model):
    """Movies' genre"""


class Person(Model):
    """Person from movie industy (actor, director)"""
    
    
class Movie(Model):
    """Movie from catalog TMDB"""
    

class MovieCredit(Model):
    """Connection between movie and users"""
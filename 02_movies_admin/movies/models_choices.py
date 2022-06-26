"""Model attributes choices for app movies."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Gender(models.TextChoices):
    """Represents TextChoices for gender attribute."""

    MALE = 'male', _('male')
    FEMALE = 'female', _('female')


class FilmworkType(models.TextChoices):
    """Represents TextChoices for filmwork type attribute."""

    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('tv_show')


class PersonRole(models.TextChoices):
    """Represents TextChoices for person role attribute."""

    ACTOR = 'actor', _('actor')
    DIRECTOR = 'director', _('director')
    WRITER = 'writer', _('writer')
